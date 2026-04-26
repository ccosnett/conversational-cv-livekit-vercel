# Conversational CV on LiveKit + Vercel

This repo runs a voice agent with:

- a Python LiveKit agent in `src/`
- a Next.js frontend in `frontend/`
- the agent deployed on LiveKit Cloud
- the frontend deployed on Vercel

The frontend connects to LiveKit directly. It does not host the Python worker.

## Repo shape

```text
.
├── src/                  # LiveKit Cloud agent
├── tests/                # Python evals/tests
├── frontend/             # Next.js voice UI for Vercel
├── livekit.toml          # LiveKit Cloud project/agent config
├── Dockerfile            # Agent build for LiveKit Cloud
└── README.md
```

## Requirements

- Python 3.10+
- `uv`
- Node.js with `corepack`
- LiveKit CLI: `brew install livekit-cli`
- a LiveKit Cloud project
- a Vercel project linked to this repo

## Environment

Agent env in root `.env.local`:

```env
LIVEKIT_URL=wss://<project-subdomain>.livekit.cloud
LIVEKIT_API_KEY=<key>
LIVEKIT_API_SECRET=<secret>
```

Frontend env for local development in `frontend/.env.local`:

```env
LIVEKIT_URL=wss://<project-subdomain>.livekit.cloud
LIVEKIT_API_KEY=<key>
LIVEKIT_API_SECRET=<secret>
AGENT_NAME=livekit-agent-minimal
```

Why `AGENT_NAME` matters:

- this repo uses explicit agent dispatch
- the deployed frontend must know which LiveKit agent to dispatch
- the current agent name is `livekit-agent-minimal`

## Local development

Install agent dependencies:

```bash
uv sync
```

Install frontend dependencies:

```bash
cd frontend
corepack pnpm install
```

Download agent model files once:

```bash
uv run python src/agent.py download-files
```

Run the agent locally:

```bash
uv run python src/agent.py dev
```

Run the frontend locally:

```bash
cd frontend
corepack pnpm dev
```

Then open `http://localhost:3000`.

## Deploy the agent to LiveKit Cloud

This repo already includes `livekit.toml` and a working `Dockerfile`.

Deploy the current agent:

```bash
lk agent deploy
```

Useful agent commands:

```bash
lk agent status
lk agent versions
lk agent logs
```

## Deploy the frontend to Vercel

Use standard Vercel Git integration. No GitHub Actions deploy workflow needed.

Vercel project settings:

- Framework Preset: `Next.js`
- Root Directory: `frontend`

Vercel env vars for both `Production` and `Preview`:

- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `LIVEKIT_URL`
- `AGENT_NAME=livekit-agent-minimal`

Expected Vercel behavior:

- push to `main` -> production deploy
- push to any other branch -> preview deploy
- PRs -> preview URLs

The repo includes `frontend/vercel.json` to pin the framework to `nextjs`.

## Monitoring in LiveKit Cloud

Use two dashboard views:

1. `Agents`
   - uptime
   - concurrent sessions
   - join latency
   - average load

2. `Sessions`
   - open a session
   - use `Agent insights`
   - inspect transcript, traces, logs, and audio recording

Agent observability must be enabled in:

- `Project Settings -> Data and privacy`

## Tests

Run Python checks:

```bash
uv run ruff check .
uv run pytest
```

Run the frontend production build:

```bash
cd frontend
corepack pnpm build
```

## Troubleshooting

### Vercel shows `404`

Check:

- Vercel framework preset is `Next.js`
- Vercel root directory is `frontend`

### Web app connects but the agent never joins

Check:

- `AGENT_NAME` is set in Vercel
- the active room shows `2` participants, not `1`
- the session shows an `Agents` badge in LiveKit Sessions

### Connected but no audio

Check:

- microphone permission in the browser
- correct input/output device
- LiveKit `Sessions -> Agent insights` for transcript/log activity

## Notes

The frontend token endpoint in `frontend/app/api/token/route.ts` is intentionally simple so Vercel preview and production deploys can issue tokens without another backend service. If this app is opened up beyond trusted/demo usage, add stronger auth around token issuance.

## References

- LiveKit Agents docs: <https://docs.livekit.io/agents/>
- LiveKit Cloud deploy docs: <https://docs.livekit.io/deploy/agents/>
- LiveKit observability docs: <https://docs.livekit.io/deploy/observability/insights/>
- Vercel project configuration: <https://vercel.com/docs/project-configuration>
