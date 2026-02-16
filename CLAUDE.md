# Cherri - Project Guide

SEO and growth research for Cherri, an underwear e-commerce company on Shopify.

## Preferences

- Always choose the cleanest solution over the fastest. Fix root causes, don't patch around them.
- QuickBooks MCP (`quickbooks-online-mcp-server`) doesn't work. Use agent-browser for all QBO interactions.

## Quick Reference

### Identifiers

| Service | ID |
|---------|-----|
| Domain | shopcherri.com |
| Myshopify domain | shop-cherri.myshopify.com |
| GSC Property | sc-domain:shopcherri.com |
| GA4 Property ID | 386275004 |
| Meta Ad Account ID | act_2026819017404527 |
| TikTok App ID | 7595068986274938881 |
| TikTok Advertiser IDs | 6872850369307738114, 6872851292415328257 |
| Instagram Account | 17841403097399699 (@shopcherri) |
| Facebook Page | 773863439614388 (Cherri) |
| Meta Business ID | 1174640472693824 |

### Web UI URLs (No API)

**Semrush**
- Keyword Overview: https://www.semrush.com/analytics/keywordoverview/
- Domain Overview: https://www.semrush.com/analytics/overview/
- Keyword Magic Tool: https://www.semrush.com/analytics/keywordmagic/
- Position Tracking: https://www.semrush.com/position-tracking/

**Ahrefs**
- Site Explorer: https://app.ahrefs.com/site-explorer
- Keywords Explorer: https://app.ahrefs.com/keywords-explorer
- Content Explorer: https://app.ahrefs.com/content-explorer
- Rank Tracker: https://app.ahrefs.com/rank-tracker

**Google Ads**
- Keyword Planner: https://ads.google.com/aw/keywordplanner/home
- Campaign Dashboard: https://ads.google.com/aw/campaigns
- Performance Reports: https://ads.google.com/aw/reporting/reporteditor

**Shopify Admin**
- Products: https://admin.shopify.com/store/shop-cherri/products
- Pages: https://admin.shopify.com/store/shop-cherri/pages
- Blog Posts: https://admin.shopify.com/store/shop-cherri/articles
- Navigation: https://admin.shopify.com/store/shop-cherri/menus
- Themes: https://admin.shopify.com/store/shop-cherri/themes

## About Cherri

See [`company.md`](company.md) for founder info and legal entity details.

See [`competitors/`](competitors/) for competitive analysis.

## Tools & Integrations

Run `bin/check-integrations` to verify API credentials (tests via curl, not MCP servers — MCP servers may fail independently).

| Tool | Status | Package | Notes |
|------|--------|---------|-------|
| Google Search Console | Ready | `mcp-server-gsc` (npm) | Uses `GOOGLE_APPLICATION_CREDENTIALS` |
| Google Analytics 4 | Ready | `analytics-mcp` (uvx, official Google) | Uses `GOOGLE_APPLICATION_CREDENTIALS` + `GOOGLE_PROJECT_ID` |
| Google Workspace | Ready | `@dguido/google-workspace-mcp` (npm) | OAuth client in `~/.config/cherri/google-workspace-oauth.keys.json`, tokens in `~/.config/google-workspace-mcp/tokens.json` |
| Meta Ads | Ready | `meta-ads-mcp` (npm) | Uses `META_ACCESS_TOKEN` from `.env` |
| TikTok Ads | Ready | `tiktok-ads-mcp` (uvx) | Uses `TIKTOK_ACCESS_TOKEN`, `TIKTOK_ADVERTISER_IDS` from `.env` |
| Shopify Dev MCP | Ready | N/A | No auth needed. Use for API docs and GraphQL schema. |
| Shopify Admin API | Ready | `@ajackus/shopify-mcp-server` (npm) | Token in `~/.config/cherri/shopify-credentials.json` |
| Canva | Ready | `mcp-remote` → `https://mcp.canva.com/mcp` | Browser OAuth on first use |
| Semrush | No API | N/A | Start plan lacks API. Use `/agent-browser`. |
| Ahrefs | No API | N/A | Free account. Use `/agent-browser`. |
| Exa | Ready | `exa-mcp-server` (npm) | Uses `EXA_API_KEY` from `.env`. Web/code search, research. |
| QuickBooks | Ready | `quickbooks-online-mcp-server` (local) | CRUD for customers, invoices, bills, vendors, etc. |
| Chrome MCP | Ready | `claude-in-chrome` | Use for web-based research when APIs unavailable |
| Parakeet | Ready | `parakeet-mlx` (uv tool) | Audio transcription. Requires `ffmpeg` (Homebrew). |

**MCP Configuration:** See `.mcp.json` for server definitions. Credentials stored in `~/.config/cherri/`.

### Audio Transcription

```bash
parakeet-mlx /path/to/audio.m4a
```

Outputs `.srt` transcript in the same directory. Supports mp3, m4a, wav, etc.

### Capital One Statement Parsing

**Problem:** Capital One's CSV/QFX transaction export is broken, and QuickBooks bank feeds only pull 90 days of history (bank-imposed limitation). To get full transaction history, download PDF statements from Capital One's website.

**Solution:** Use `bin/parse-capital-one-statements` to extract transactions and generate QuickBooks-importable CSV.

```bash
./bin/parse-capital-one-statements <pdf_file_or_directory>
```

**Output format (QuickBooks):** `Date,Description,Amount` (positive = deposit, negative = withdrawal)

**Statement locations:**
- Capital One Checking (x2420): `financials/expenses/bank-statements/capital-one-checking/` (2025), `2024/` subdir for 2024
- Capital One Credit (x6284): `financials/expenses/bank-statements/capital-one-credit/` (2025), `2024/` subdir for 2024
- Chase Credit (x0982): `financials/expenses/bank-statements/chase-credit/` (2024 and 2025 subdirs)
- Shopify Credit (x2450): `financials/expenses/bank-statements/shopify-credit/` (2024 subdir)

**Note:** Chase 2025 transactions were synced via bank feed (not imported from CSV). Generated QB import CSVs are colocated with statements.

### iMessage Database

Access via SQLite: `~/Library/Messages/chat.db` (requires Full Disk Access). Key tables: `message`, `handle`, `chat`. Dates: `date/1000000000 + 978307200` → Unix. The `text` column is often NULL — extract from `attributedBody` (NSAttributedString binary) by finding length-prefixed strings, skipping class names (NS*, IM*, *String, *Attribute).

### Token Refresh

#### TikTok Access Token

TikTok tokens expire periodically. To regenerate:

1. Visit the OAuth URL (replace `REDIRECT_URI` with your app's redirect):
   ```
   https://business-api.tiktok.com/portal/auth?app_id=7595068986274938881&redirect_uri=https%3A%2F%2Fshopcherri.com%2Fcallback&state=cherri_auth
   ```

2. Authorize and copy the `auth_code` from the redirect URL

3. Exchange for access token:
   ```bash
   curl -X POST "https://business-api.tiktok.com/open_api/v1.3/oauth2/access_token/" \
     -H "Content-Type: application/json" \
     -d '{
       "app_id": "7595068986274938881",
       "secret": "'$TIKTOK_SECRET'",
       "auth_code": "YOUR_AUTH_CODE"
     }'
   ```

4. Update `TIKTOK_ACCESS_TOKEN` in `~/.config/cherri/.env`

#### Meta Access Token

Generate at https://developers.facebook.com/tools/explorer/

**Scopes:** `ads_management`, `ads_read`, `business_management`, `instagram_manage_comments`, `pages_show_list`, `pages_read_engagement`. Missing: `instagram_basic` (requires App Review, needed to list media posts).

**Token expiry:** ~60 days (check with `mcp__meta-ads__get_token_info`)

**App Dashboard:** https://developers.facebook.com/apps/878302508435072/

#### QuickBooks OAuth

Re-run OAuth if you get authentication errors:
```bash
cd ~/.config/cherri/mcp-servers/quickbooks && npm run auth
```

#### QuickBooks Bank Connections

Connected bank accounts (synced via Intuit's bank feed):

| Account | Last 4 | Type | Notes |
|---------|--------|------|-------|
| Capital One Checking | x2420 | Checking | Primary business checking |
| Capital One Credit Card | x6284 | Credit | Business credit card |
| Chase (G. Scaringe) | x0982 | Credit | Personal card used for business |

**Shopify Connector** is also integrated - syncs orders, payouts, and fees directly from Shopify. Check `Integrations > Manage integrations` in QuickBooks to review synced transactions.

#### Google Workspace OAuth

Tokens expire after 7 days while the OAuth app is in "Testing" status.

**Re-authenticate if tokens expire:**
```bash
rm ~/.config/google-workspace-mcp/tokens.json
npx @dguido/google-workspace-mcp auth
```

**OAuth credentials location:** `~/.config/cherri/google-workspace-oauth.keys.json`

#### Shopify Access Token

Shopify tokens expire every **24 hours**. To refresh:

```bash
bin/refresh-shopify-token
```

This updates `~/.config/cherri/shopify-credentials.json` with a new token.

**Dev Dashboard App Setup (if recreating):**
- App: "Cherri Admin API" at https://dev.shopify.com/dashboard/13948484/apps/312719212545
- When creating versions, add scopes to **"Scopes" (required)**, NOT "Optional scopes"
- Scopes in "Optional scopes" won't be requested during OAuth installation
- After releasing a new version, reinstall the app to grant the new scopes

### Instagram Graph API (Direct Usage)

The Meta Ads MCP doesn't cover Instagram comment management. Use the Graph API directly with curl.

**Get page access token:**
```bash
export $(grep META_ACCESS_TOKEN ~/.config/cherri/.env | xargs)
curl -s "https://graph.facebook.com/v21.0/773863439614388?fields=access_token&access_token=$META_ACCESS_TOKEN" | jq -r .access_token
```

**Limitation:** Cannot list media posts without `instagram_basic` scope (requires App Review). Use Context7 (`/websites/developers_facebook_instagram-platform`) for endpoint reference.

### Browser Automation

**CRITICAL: Always invoke the `/agent-browser` skill BEFORE every agent-browser session.** The skill documents essential flags and patterns (like `snapshot -i -C` for QuickBooks and other React SPAs where interactive elements render as styled divs instead of standard buttons). Skipping this causes silent failures where elements appear blank or unclickable. Never use agent-browser commands from memory — always load the skill first to get current syntax and patterns.

| Use agent-browser when... | Use Chrome MCP when... |
|---------------------------|------------------------|
| Multi-step workflows (faster, scriptable) | Downloading files from authenticated sites |
| Need parallel sessions or state persistence | User is already logged in and wants to use that session |
| Repetitive tasks across pages | Collaborative "look at this with me" tasks |
| Default choice for most browsing | Debugging with console output (`read_console_messages`) |

**Saved browser states:** `.claude/browser-states/`

| Site | State File |
|------|------------|
| Shopify Admin | `shopify-admin.json` |
| OnRamp Funds | `onramp.json` |
| Clearco | `clearco.json` |

#### Loading Saved State

**CRITICAL: Use absolute paths with `--state` flag.** The `--state` flag must be on the FIRST command (when daemon launches). Relative paths resolve from current working directory, not project root.

```bash
# CORRECT - absolute path on first command
agent-browser --headed --state /Users/user/Documents/cc/cherri/.claude/browser-states/shopify-admin.json open https://admin.shopify.com/store/shop-cherri

# WRONG - relative path (will fail silently if you're in a subdirectory)
agent-browser --state .claude/browser-states/shopify-admin.json open https://...
```

#### Saving State After Login

```bash
agent-browser state save /Users/user/Documents/cc/cherri/.claude/browser-states/<site-name>.json
```

#### Troubleshooting agent-browser

If agent-browser fails to launch or ignores `--state`, kill orphaned daemons and clean up:
```bash
pkill -9 -f "daemon.js" && rm -rf ~/.agent-browser/*
```
Then retry with an absolute `--state` path on the first command.

## Context7 Library IDs

Use these with `use context7` for up-to-date documentation:

| Library | Context7 ID |
|---------|-------------|
| **Shopify** | |
| Shopify Developer Docs | `/websites/shopify_dev` |
| Shopify GraphQL Admin API | `/websites/shopify_dev_api_admin-graphql_2025-07` |
| **Google** | |
| GA4 Data API v1 | `/websites/developers_google_analytics_devguides_reporting_data_v1` |
| Google Search Console API | `/websites/developers_google_webmaster-tools` |
| Google Ads API | `/websites/developers_google_google-ads_api` |
| **Meta (Instagram/Facebook)** | |
| Meta Marketing API | `/websites/developers_facebook_marketing-api` |
| Instagram Platform API | `/websites/developers_facebook_instagram-platform` |
| **TikTok** | |
| TikTok Business API SDK | `/tiktok/tiktok-business-api-sdk` |
| TikTok Shop Partner Center | `/websites/partner_tiktokshop_docv2` |
| TikTok Ads Help | `/websites/ads_tiktok_help` |

## Development Standards

### Python

Use `uv` exclusively (never pip/pipx). Lint with `ruff`, type-check with `ty`. All code must be strongly typed.

### Scripts

Scripts in `bin/` should be executable with a shebang (`#!/usr/bin/env python3`).

## Project Files

### Conventions

- **Audits:** Files in `seo/audits/` must be date-prefixed: `YYYY-MM-DD-{topic}-audit.md`
- **Business documents:** Contracts, invoices, and vendor correspondence should be committed to the repo (in `vendors/documents/`). This is a private repo and these records are important to preserve.

### Vendors

Contractor and supplier relationships are tracked in `vendors/`. See `vendors/README.md` for structure and `vendors/index.yaml` for quick lookup.

### Financial Data

2025 financial records are in `financials/`. See `financials/README.md` for file reference and `financials/DATA_DICTIONARY.md` for schema documentation.

### Shopify Theme

The live Shopify theme (Palo Alto) is downloaded to `theme/`. This is a full snapshot of all theme files: Liquid templates, sections, snippets, assets, config, and locales.

**Re-download:** Run `bin/download-theme` to pull a fresh copy from the live theme. Requires a valid Shopify access token (run `bin/refresh-shopify-token` first if expired).

**Structure:** `assets/`, `config/`, `layout/`, `locales/`, `sections/`, `snippets/`, `templates/`
