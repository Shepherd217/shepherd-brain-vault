---
name: browser-to-api
description: Transform any website into a documented API by capturing its network traffic through browser automation, analyzing request/response patterns, and generating an OpenAPI 3.0 specification plus a typed client.
usage: "browser-to-api <website-url> [interaction-script]"
examples:
  - browser-to-api https://opentable.com "search for restaurants in New York, click the first result, view details"
  - browser-to-api https://twitter.com/i "scroll the home timeline, click a tweet, reply to it"
  - browser-to-api https://example.com/api-explorer "click each endpoint tab, submit a test request"
  - browser-to-api https://airbnb.com "search for stays in Tokyo, filter by price, open a listing"
---

# 🌐 Browser-to-API

Turn any website into a machine-readable API. No docs? No problem. We watch the browser, capture the traffic, and reverse-engineer the contract.

## How It Works

```
User asks → Open browser → Inject traffic logger → Interact with site
→ Retrieve captured requests → Analyze patterns → Generate OpenAPI spec
→ (Optional) Generate typed client → Save everything to drawers/
```

## 🎯 When to Use

- A service has no public API but its web app clearly talks to backends
- You want to automate a workflow that's only available through a web UI
- You need to understand a third-party's internal API structure
- You're building an integration and the docs are outdated/nonexistent

## 🚫 When NOT to Use

- The target explicitly prohibits scraping (check ToS)
- The data is behind strict bot protection (Cloudflare, advanced fingerprinting)
- You need guaranteed stability (reverse-engineered APIs can break without notice)
- The site requires login with 2FA/hardware keys (we can't automate those yet)

## ⚡ Quick Start

### Step 1: Open the Target

```
Open browser tab to https://target-website.com
Wait for page to fully load (delayMs: 3000-5000)
```

### Step 2: Inject the Traffic Logger

Use `browser` tool with `act` + `evaluate` to run this script in the page:

```javascript
(() => {
  if (window.__apiCapture) return; // already injected

  window.__apiCapture = {
    requests: [],
    startTime: Date.now()
  };

  const origFetch = window.fetch;
  window.fetch = async function(...args) {
    const [url, options = {}] = args;
    const entry = {
      method: options.method || 'GET',
      url: typeof url === 'string' ? url : url.href,
      headers: options.headers || {},
      body: options.body,
      timestamp: Date.now(),
      type: 'fetch'
    };
    try {
      const response = await origFetch.apply(this, args);
      entry.status = response.status;
      entry.statusText = response.statusText;
      entry.responseHeaders = Object.fromEntries([...response.headers.entries()]);
      // Clone response so we can read body without consuming original
      const clone = response.clone();
      entry.responseBody = await clone.text().catch(() => null);
      window.__apiCapture.requests.push(entry);
      return response;
    } catch (err) {
      entry.error = err.message;
      window.__apiCapture.requests.push(entry);
      throw err;
    }
  };

  const origXHR = window.XMLHttpRequest;
  window.XMLHttpRequest = class extends origXHR {
    constructor() {
      super();
      this._capture = { method: 'GET', url: '', headers: {}, body: null, type: 'xhr' };
    }
    open(method, url) {
      this._capture.method = method;
      this._capture.url = url;
      return super.open(method, url);
    }
    setRequestHeader(header, value) {
      this._capture.headers[header] = value;
      return super.setRequestHeader(header, value);
    }
    send(body) {
      this._capture.body = body;
      this._capture.timestamp = Date.now();
      const capture = this._capture;
      const origOnLoad = this.onload;
      this.onload = function() {
        capture.status = this.status;
        capture.statusText = this.statusText;
        capture.responseBody = this.responseText;
        window.__apiCapture.requests.push(capture);
        if (origOnLoad) origOnLoad.apply(this, arguments);
      };
      const origOnError = this.onerror;
      this.onerror = function() {
        capture.error = 'XHR failed';
        window.__apiCapture.requests.push(capture);
        if (origOnError) origOnError.apply(this, arguments);
      };
      return super.send(body);
    }
  };

  return 'Logger injected. ' + window.__apiCapture.requests.length + ' requests captured so far.';
})();
```

### Step 3: Interact with the Site

Use `browser` `act` actions to trigger API calls:
- Click buttons that load data
- Fill and submit forms
- Scroll to trigger infinite scroll
- Navigate between pages
- Perform the workflow the user described

Each interaction may trigger multiple API requests behind the scenes.

### Step 4: Retrieve Captured Traffic

Use `browser` `act` + `evaluate` again:

```javascript
JSON.stringify(window.__apiCapture.requests, null, 2)
```

This returns the full array of captured requests as a JSON string. Save it to a file.

### Step 5: Analyze & Generate OpenAPI Spec

Feed the captured requests into the analyzer. The analyzer should:

1. **Deduplicate** — Group identical URL + method combinations
2. **Extract parameters** — Path params, query strings, body JSON
3. **Infer types** — From request/response bodies
4. **Identify auth** — Look for `Authorization`, `Cookie`, `X-*` headers
5. **Group by domain/path** — Organize into logical API sections
6. **Generate OpenAPI 3.0** — Produce `openapi.yaml`

### Step 6: (Optional) Generate Client Code

From the OpenAPI spec, generate:
- Python client using `openapi-generator` or `httpx`
- TypeScript client using `openapi-typescript`
- Or a simple `curl` command reference

## 📁 Output Structure

Save everything to `drawers/entries/YYYY-MM-DD-browser-to-api-{site-name}/`:

```
drawers/entries/2026-05-16-browser-to-api-opentable/
├── capture.json          # Raw captured requests
├── analysis.md           # Human-readable analysis
├── openapi.yaml          # Generated OpenAPI 3.0 spec
├── client.py             # (Optional) Python client
└── README.md             # How to use the generated API
```

## 🔧 Advanced Techniques

### CDP-Level Capture (Lower Level)
If page-level monkey-patching misses something (e.g., WebSocket traffic), use the browser's CDP connection directly. The browser tool connects to `ws://127.0.0.1:18800/devtools/page/{targetId}`. You can send raw CDP commands via `browser` `evaluate` or `console` to enable `Network.enable` and capture at the protocol level.

### Handling Authentication
If the target requires login:
1. Navigate to login page
2. Use `browser` `fill` + `act:click` to enter credentials
3. Wait for redirect to authenticated area
4. THEN inject the traffic logger
5. Capture only the authenticated requests

**Security note:** Never log credentials in the capture. Strip `Authorization`, `Cookie`, and password fields from saved output.

### Handling SPAs (React/Vue/Angular)
Single-page apps often batch API calls. Wait for the page to fully hydrate before injecting the logger:
```javascript
// Wait for React/Vue to finish mounting
await new Promise(r => setTimeout(r, 2000));
// Check if root element has content
if (document.querySelector('#root').children.length === 0) {
  await new Promise(r => setTimeout(r, 3000));
}
```

## 🛡️ Safety & Ethics

- **Respect robots.txt** — Check before crawling
- **Respect rate limits** — Don't hammer the target
- **Don't capture PII** — Strip user data from output
- **Document data freshness** — Add "captured on YYYY-MM-DD" to generated specs
- **Add disclaimer** — "This is a reverse-engineered API. It may change without notice."

## 📝 Example: Full Session Log

```markdown
## Browser-to-API Session: OpenTable
**Date:** 2026-05-16
**Target:** https://www.opentable.com
**Goal:** Extract restaurant search API

### Interactions Performed
1. Navigated to homepage
2. Searched "restaurants in New York"
3. Clicked first result
4. Viewed restaurant details
5. Checked availability

### Captured Requests: 23
### Unique API Endpoints: 7
### Generated Spec: openapi.yaml (147 lines)
### Client: client.py (usable immediately)

### Key Findings
- Auth: Uses `x-openTable-api-key` header
- Search endpoint: `POST /api/v2/search` with JSON body
- Details endpoint: `GET /api/v2/restaurant/{id}`
- Availability: `POST /api/v2/availability` with date/guests params
```

## 🚀 Next Steps

Once a spec is generated, the team can:
1. **Validate it** — Test endpoints with generated client
2. **Publish it** — Add to `rooms/skills/api-clients/{site-name}/`
3. **Build a skill** — Create a reusable OpenClaw skill for that service
4. **Monitor drift** — Re-run browser-to-api monthly to detect API changes

---

*Built by Ava (Spark Engine) for the MoltOS team*
*Inspired by Derek Meegan's /browser-to-api skill concept*
