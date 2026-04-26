import React from 'react';
import { AnimatePresence, type MotionProps, motion } from 'motion/react';
import { cn } from '@/lib/shadcn/utils';
import { AudioVisualizer } from './audio-visualizer';

const ANIMATION_TRANSITION: MotionProps['transition'] = {
  type: 'spring',
  stiffness: 675,
  damping: 75,
  mass: 1,
};

const tileViewClassNames = {
  grid: ['h-full w-full', 'grid place-content-center grid-rows-[90px_1fr_90px]'],
  agentChatOpen: ['row-start-1', 'place-content-center'],
  agentChatClosed: ['row-start-1 row-span-3', 'place-content-center'],
};

interface TileLayoutProps {
  chatOpen: boolean;
  audioVisualizerType?: 'bar' | 'wave' | 'grid' | 'radial' | 'aura';
  audioVisualizerColor?: `#${string}`;
  audioVisualizerColorShift?: number;
  audioVisualizerWaveLineWidth?: number;
  audioVisualizerGridRowCount?: number;
  audioVisualizerGridColumnCount?: number;
  audioVisualizerRadialBarCount?: number;
  audioVisualizerRadialRadius?: number;
  audioVisualizerBarCount?: number;
}

export function TileLayout({
  chatOpen,
  audioVisualizerType,
  audioVisualizerColor,
  audioVisualizerColorShift,
  audioVisualizerBarCount,
  audioVisualizerRadialBarCount,
  audioVisualizerRadialRadius,
  audioVisualizerGridRowCount,
  audioVisualizerGridColumnCount,
  audioVisualizerWaveLineWidth,
}: TileLayoutProps) {
  const animationDelay = chatOpen ? 0 : 0.15;

  return (
    <div className="absolute inset-x-0 top-8 bottom-32 z-50 md:top-12 md:bottom-40">
      <div className="relative mx-auto h-full max-w-2xl px-4 md:px-0">
        <div className={cn(tileViewClassNames.grid)}>
          <div
            className={cn([
              'grid',
              chatOpen ? tileViewClassNames.agentChatOpen : tileViewClassNames.agentChatClosed,
            ])}
          >
            <AnimatePresence mode="popLayout">
              <motion.div
                key="agent"
                layoutId="agent"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{
                  ...ANIMATION_TRANSITION,
                  delay: animationDelay,
                }}
                className="relative aspect-square h-[90px]"
              >
                <AudioVisualizer
                  key="audio-visualizer"
                  initial={{ scale: 1 }}
                  animate={{ scale: chatOpen ? 0.2 : 1 }}
                  transition={{
                    ...ANIMATION_TRANSITION,
                    delay: animationDelay,
                  }}
                  audioVisualizerType={audioVisualizerType}
                  audioVisualizerColor={audioVisualizerColor}
                  audioVisualizerColorShift={audioVisualizerColorShift}
                  audioVisualizerBarCount={audioVisualizerBarCount}
                  audioVisualizerRadialBarCount={audioVisualizerRadialBarCount}
                  audioVisualizerRadialRadius={audioVisualizerRadialRadius}
                  audioVisualizerGridRowCount={audioVisualizerGridRowCount}
                  audioVisualizerGridColumnCount={audioVisualizerGridColumnCount}
                  audioVisualizerWaveLineWidth={audioVisualizerWaveLineWidth}
                  isChatOpen={chatOpen}
                  className={cn(
                    'absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2',
                    'bg-background rounded-[50px] border border-transparent transition-[border,drop-shadow]',
                    chatOpen && 'border-input shadow-2xl/10 delay-200'
                  )}
                  style={{ color: audioVisualizerColor }}
                />
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}
