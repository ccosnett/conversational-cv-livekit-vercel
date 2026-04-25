# intention.md

## Purpose

This repo is the Vercel-focused continuation of the current working
`livekit-agent-minimal` setup.

Keep the original repo untouched.
Use this repo to ship the web app cleanly.

## Current architecture

- Python LiveKit agent worker in `src/`
- agent deployed on LiveKit Cloud
- Next.js frontend in `frontend/`
- frontend talks to LiveKit; does not host the Python worker

## Immediate goal

Deploy the current frontend to Vercel with the least possible product churn.

Meaning:

1. keep the LiveKit worker architecture intact
2. keep the working browser flow intact
3. make the web app deployable and testable on Vercel
4. avoid mixing "frontend simplification" with "deployment rescue"

## Constraints

- no secrets in git
- leave `livekit-agent-minimal` alone
- keep changes reviewable
- preserve the currently working local flow before simplifying UI

## Known reality

The frontend currently works locally.

Important caveat:

- `frontend/app/api/token/route.ts` is explicitly development-only
- it throws in non-development environments
- production deployment needs a proper token strategy before Vercel can serve
  the app end-to-end

## Deployment target

Deploy the Next.js app in `frontend/` to Vercel.

Expected Vercel project shape:

- framework: Next.js
- root directory: `frontend`
- env vars:
  - `LIVEKIT_URL`
  - `LIVEKIT_API_KEY`
  - `LIVEKIT_API_SECRET`
  - `AGENT_NAME`

## Planned work

1. import this repo into Vercel with `frontend/` as the root
2. replace or secure the current dev-only token route
3. verify the deployed app can dispatch the LiveKit agent by `AGENT_NAME`
4. add minimal production docs for deploy + rollback
5. only then simplify the starter UI

## Non-goals

- rewriting the Python agent first
- changing the LiveKit Cloud deployment model
- adding extra backend services unless forced by auth/security needs
- broad product redesign before deploy works

## Definition of done

Good outcome:

- Vercel deployment succeeds
- app loads from a public URL
- user can start a session from the deployed frontend
- deployed frontend connects to the existing LiveKit agent reliably
- deployment steps are documented in this repo
