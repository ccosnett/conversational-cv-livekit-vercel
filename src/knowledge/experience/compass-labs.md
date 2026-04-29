# Compass Labs

At Compass Labs I was most recently a Founding Engineer at an Andreessen
Horowitz-backed DeFi infrastructure startup.

Core facts:

- I built and maintained a universal DeFi API in Python using FastAPI and
  Pydantic.
- I shipped production endpoints that returned unsigned EVM transactions so
  users could execute DeFi flows while the product stayed non-custodial.
- I built CI/CD pipelines that generated and tested downstream Python and
  TypeScript SDKs from OpenAPI specs.
- I designed custom analytics endpoints around Aave, including interest rates,
  volatility, utilization, TVL, and historical transactions.
- I researched EVM transaction bundling and demonstrated large gas savings.
- I contributed heavily in a short period, with over 1000 GitHub contributions
  in 11 months, including a merged LangChain contribution.
- I led developer-relations engineering work, including educational material
  and videos for enterprise users such as MoonPay.
- I proposed and drove product features such as intention-based API design,
  gasless endpoints, allowance-free UX, and embedded transaction bundling.

Agentic systems context:

- we built a natural-language blockchain transaction agent
- we built a Logfire-powered monitoring agent that summarized user issues and
  alerted the team in Slack
- I came up with the initial MVP direction for both of those systems

## Product instinct and simplification

One of the clearest product-instinct signals from Compass is that Conor did not
just ship features. He pushed to simplify the company and the API around the
core user problem.

### Simplifying the company offering

According to Conor's own account:

- the company had spread itself across too many products
- one of those products was a blockchain backtesting and simulation system
  called Dojo
- Dojo was expensive to maintain because protocol changes kept forcing updates
- it absorbed a lot of engineering effort from strong engineers

He persuaded the team to stop focusing on that project and concentrate on the
core API product instead.

That matters because it shows:

- willingness to cut scope
- understanding that focus is a product decision
- sensitivity to engineering cost, not just technical possibility

### Simplifying the API itself

He also describes the API as having bloated to more than 100 endpoints.

His proposal was to simplify the product into a smaller number of high-level
endpoints that were more intuitive and could do more useful work.

The key idea was to move from low-level blockchain operations toward
intention-based API design.

Example framing:

- instead of forcing users to know atomic blockchain operations in advance
- let them express a higher-level goal such as "I want to earn yield on my
  stablecoin"
- let the system figure out the underlying implementation details

Related ideas he proposed around the same product direction:

- organize the API by intention rather than by protocol
- make endpoints gasless where possible
- avoid forcing users to manage allowances directly
- preserve non-custodial behavior while increasing abstraction
- use bundling throughout the product where appropriate

### Why this is a strong product signal

This is not just "I had an idea." It shows a recognizable pattern:

- reduce product sprawl
- collapse a large surface area into a smaller, more legible abstraction
- remove protocol-level thinking from the user experience
- preserve technical constraints while making the product easier to use

This suggests Conor has taste for:

- simplification
- abstraction
- user-facing clarity
- product decisions that reduce cognitive load

### Gen AI and tool-use direction

He also says he introduced the team more deeply to Gen AI thinking and built a
prototype agent that could operate the API through tool calls.

This matters because it extends the same product instinct:

- the API should not only be powerful for technical users
- it should also become accessible to non-technical users through a higher-level
  interface
