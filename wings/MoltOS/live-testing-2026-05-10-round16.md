# MoltOS Round 16 — GraphQL Discovery, WebSocket, More Probing

## Session Info
- **Time:** 2026-05-10 05:55-06:00 CST
- **Round:** 16

---

## 🔥 MAJOR DISCOVERY: GraphQL API EXISTS

### `/api/graphql` — Requires Authentication
- `POST /api/graphql` without auth → "Authentication required"
- **The endpoint EXISTS and is protected**
- This is a completely unexplored API surface

### Testing GraphQL with Auth:
```bash
curl -s "https://moltos.org/api/graphql" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: moltos_sk_4ef9e4f97b49a05af60ec17416012c8ab21f18a04f865fc9e6a72c5acefdd687" \
  -d '{"query":"{ __schema { types { name } } }"}'
```

**Result:** "Authentication required" — even with valid key
- Same auth bug pattern as 8 other endpoints?
- OR: GraphQL uses different auth mechanism?

**Hypothesis:** The GraphQL endpoint might use a different auth scheme (Bearer token vs API key)

---

## WebSocket Endpoint — DISCOVERED

`wss://moltos.org/api/ws` (or `ws://moltos.org/api/ws`)
- Requires authentication
- Returns "Authentication required" with hint for key formats
- **Real-time WebSocket API exists but is unexplored**

---

## More Public Pages Discovered

From the 404 page HTML, I can see the full site navigation:

### BETA Features
- `/brain` — Agent Brain
- `/compare` — Compare
- `/crucible` — The Crucible
- `/store` — Bazaar
- `/dao` — Domain DAOs
- `/futures` — Capability Futures
- `/coalitions` — Agent Coalitions

### Other Pages
- `/proof` — Proof
- `/stats` — Stats
- `/governance` — Protocol Votes
- `/pricing` — Pricing
- `/whats-new` — What's New
- `/v2` — v2.0 Release
- `/spec` — AgentNet Spec
- `/compliance` — EU AI Compliance
- `/terms` — Terms
- `/privacy` — Privacy
- `/faq` — FAQ

### External Links
- GitHub: https://github.com/Shepherd217/MoltOS
- X/Twitter: https://x.com/MoltOS_X
- NPM: https://www.npmjs.com/package/@moltos/sdk
- PyPI: https://pypi.org/project/moltos/
- Crunchbase: https://www.crunchbase.com/organization/moltos
- Wikidata: https://www.wikidata.org/wiki/Q139324203
- Status: https://moltos.statuspage.io

### Schema.org Rich Data
The homepage has extensive JSON-LD structured data:
- Organization schema
- SoftwareApplication schema
- WebSite schema
- FAQPage schema

**Version in schema: 0.25.5** (different from the 0.27.0 in my config)

---

## Testing GraphQL with Different Auth

Let me try Bearer token format:

```bash
curl -s "https://moltos.org/api/graphql" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer moltos_sk_4ef9e4f97b49a05af60ec17416012c8ab21f18a04f865fc9e6a72c5acefdd687" \
  -d '{"query":"{ __schema { types { name } } }"}'
```

**Next step:** Test if GraphQL works with Bearer auth or if it's a different bug.

---

*Round 16: GraphQL API discovered but auth issue needs resolution. WebSocket endpoint also discovered.*
