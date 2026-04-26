'use client';

import { useMemo } from 'react';
import { TokenSource } from 'livekit-client';
import { useSession } from '@livekit/components-react';
import { WarningIcon } from '@phosphor-icons/react/dist/ssr';
import type { AppConfig } from '@/app-config';
import { AgentSessionProvider } from '@/components/agents-ui/agent-session-provider';
import { StartAudioButton } from '@/components/agents-ui/start-audio-button';
import { ViewController } from '@/components/app/view-controller';
import { Toaster } from '@/components/ui/sonner';
import { useAgentErrors } from '@/hooks/useAgentErrors';
import { useDebugMode } from '@/hooks/useDebug';

const IN_DEVELOPMENT = process.env.NODE_ENV !== 'production';

function AppSetup() {
  useDebugMode({ enabled: IN_DEVELOPMENT });
  useAgentErrors();

  return null;
}

interface AppProps {
  appConfig: AppConfig;
}

export function App({ appConfig }: AppProps) {
  const sessionSeed = useMemo(() => crypto.randomUUID(), []);
  const tokenSource = useMemo(() => {
    return TokenSource.custom(async (options) => {
      const roomConfig = options.agentName
        ? {
            agents: [
              {
                agentName: options.agentName,
                metadata: options.agentMetadata ?? '',
              },
            ],
          }
        : undefined;

      const res = await fetch('/api/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          room_name: options.roomName ?? `voice_assistant_room_${sessionSeed}`,
          participant_identity:
            options.participantIdentity ?? `voice_assistant_user_${sessionSeed}`,
          participant_name: options.participantName ?? 'user',
          participant_metadata: options.participantMetadata,
          participant_attributes: options.participantAttributes,
          room_config: roomConfig,
        }),
      });

      if (!res.ok) {
        throw new Error(`Error generating token: ${res.status} ${await res.text()}`);
      }

      return await res.json();
    });
  }, [sessionSeed]);

  const session = useSession(
    tokenSource,
    appConfig.agentName ? { agentName: appConfig.agentName } : undefined
  );

  return (
    <AgentSessionProvider session={session}>
      <AppSetup />
      <main className="grid h-svh grid-cols-1 place-content-center">
        <ViewController appConfig={appConfig} />
      </main>
      <StartAudioButton label="Start Audio" />
      <Toaster
        icons={{
          warning: <WarningIcon weight="bold" />,
        }}
        position="top-center"
        className="toaster group"
        style={
          {
            '--normal-bg': 'var(--popover)',
            '--normal-text': 'var(--popover-foreground)',
            '--normal-border': 'var(--border)',
          } as React.CSSProperties
        }
      />
    </AgentSessionProvider>
  );
}
