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

Run `bin/check-integrations` to verify API credentials are working.

> **Note:** `bin/check-integrations` tests API credentials directly via curl, not MCP servers. MCP servers may fail even if credentials work (e.g., wrong package name).

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

Transcribe voicemails and audio files using parakeet-mlx (NVIDIA's Parakeet model optimized for Apple Silicon):

```bash
parakeet-mlx /path/to/audio.m4a
```

Outputs `.srt` transcript in the same directory. Supports mp3, m4a, wav, etc.

### Capital One Statement Parsing

**Problem:** Capital One's CSV/QFX transaction export is broken, and QuickBooks bank feeds only pull 90 days of history (bank-imposed limitation). To get full transaction history, download PDF statements from Capital One's website.

**Solution:** Use `bin/parse-capital-one-statements` to extract transactions and generate QuickBooks-importable CSV.

```bash
# Parse single statement
./bin/parse-capital-one-statements <pdf_file>

# Parse all statements in directory
./bin/parse-capital-one-statements financials/expenses/bank-statements/capital-one-checking/

# Output to specific file
./bin/parse-capital-one-statements <path> --output transactions.csv

# Detailed output with separate deposit/withdrawal/balance columns
./bin/parse-capital-one-statements <path> --detailed
```

**Output format (QuickBooks):** `Date,Description,Amount` (positive = deposit, negative = withdrawal)

**Statement locations:**
- Capital One Checking (x2420): `financials/expenses/bank-statements/capital-one-checking/` (2025), `2024/` subdir for 2024
- Capital One Credit (x6284): `financials/expenses/bank-statements/capital-one-credit/` (2025), `2024/` subdir for 2024
- Chase Credit (x0982): `financials/expenses/bank-statements/chase-credit/` (2024 and 2025 subdirs)
- Shopify Credit (x2450): `financials/expenses/bank-statements/shopify-credit/` (2024 subdir)

**Generated QB imports:**
- `capital-one-checking/2025_qb_import.csv` (2,614 transactions)
- `capital-one-checking/2024/2024_checking_q{1-4}_qb_import.csv` (2,118 transactions, split quarterly)
- `capital-one-credit/2025_qb_import.csv` (45 transactions)
- `capital-one-credit/2024/2024_credit_qb_import.csv` (39 transactions)
- `chase-credit/2024/2024_chase_qb_import.csv` (31 transactions)
- `shopify-credit/2024/2024_shopify_credit_qb_import.csv` (115 transactions)

**Note:** Chase 2025 transactions were synced via bank feed (not imported from CSV).

**How the parser works:**
- Uses `pdfplumber` (installed via `uv tool install pdfplumber`) to extract text
- Auto-detects statement type (checking vs credit card) based on content
- Handles year-spanning billing cycles (e.g., Dec 2024 - Jan 2025) correctly
- Classifies deposits vs withdrawals using keyword matching (Shopify transfers = deposits, Shopify Capital/Credit = withdrawals, etc.)
- Deduplicates transactions when parsing multiple overlapping statements

**Raw text extraction (for debugging):**
```bash
uvx pdfplumber /path/to/statement.pdf --format text
```

**Fallback:** If pdfplumber doesn't extract tables cleanly, use [Mistral OCR API](https://docs.mistral.ai/capabilities/document_ai/basic_ocr) ($2/1000 pages) with `table_format="html"` for complex tables.

### iMessage Database

Access iMessages via SQLite at `~/Library/Messages/chat.db`. Requires Full Disk Access for terminal.

**Key tables:** `message`, `handle` (contacts), `chat`

**Date conversion:** `date/1000000000 + 978307200` → Unix timestamp

**Text extraction:** The `text` column is often NULL. Use `attributedBody` (NSAttributedString binary). Extract by finding length-prefixed strings in the blob, skipping class names (NS*, IM*, *String, *Attribute).

**Example query:**
```sql
SELECT datetime(m.date/1000000000 + 978307200, 'unixepoch', 'localtime') as date,
       CASE WHEN m.is_from_me = 1 THEN 'Me' ELSE 'Them' END as sender,
       m.text, m.attributedBody
FROM message m
JOIN handle h ON m.handle_id = h.rowid
WHERE h.id LIKE '%5551234567%'
ORDER BY m.date DESC;
```

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

**Current scopes:**
- `ads_management`, `ads_read` - Meta Ads API
- `business_management` - Business account access
- `instagram_manage_comments` - Read/reply/delete Instagram comments
- `pages_show_list`, `pages_read_engagement` - Facebook Page access

**Missing scopes (requires App Review):**
- `instagram_basic` - List Instagram media posts (needed to discover media IDs)

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

The Google Workspace MCP provides access to Gmail, Drive, Docs, Sheets, Slides, Calendar, and Contacts. Tokens expire after 7 days while the OAuth app is in "Testing" status.

**Re-authenticate if tokens expire:**
```bash
rm ~/.config/google-workspace-mcp/tokens.json
npx @dguido/google-workspace-mcp auth
```

**OAuth credentials location:** `~/.config/cherri/google-workspace-oauth.keys.json`

**To create new OAuth credentials (if needed):**
1. Go to [GCP Credentials](https://console.cloud.google.com/apis/credentials?project=cherri-seo-research)
2. Click **+ CREATE CREDENTIALS** > **OAuth client ID**
3. Select **Desktop app**, name it `Google Workspace MCP`
4. Download JSON and save to `~/.config/cherri/google-workspace-oauth.keys.json`

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

**API endpoints (require media ID):**
```bash
# List comments on a media post
GET /{media-id}/comments?fields=id,text,username,timestamp

# Reply to a comment
POST /{comment-id}/replies?message=Thank+you!

# Delete/hide a comment
DELETE /{comment-id}

# Like a comment (if supported)
POST /{comment-id}/likes
```

**Current limitation:** Cannot list media posts without `instagram_basic` scope. Must know media ID in advance or use Chrome MCP to browse Meta Business Suite.

**Context7 docs:** Use `/websites/developers_facebook_instagram-platform` for API reference.

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

**Verify the state file exists before using:**
```bash
ls -la /Users/user/Documents/cc/cherri/.claude/browser-states/shopify-admin.json
```

#### Saving State After Login

```bash
agent-browser state save /Users/user/Documents/cc/cherri/.claude/browser-states/<site-name>.json
```

#### Troubleshooting agent-browser

**Symptom:** `"Browser not launched. Call launch first"` error

**Cause:** This cryptic error usually means one of:
1. The `--state` file path doesn't exist (most common)
2. Orphaned daemon processes from a previous failed launch
3. Stale PID/socket files in `~/.agent-browser/`

**Fix:**
```bash
# 1. Kill any orphaned daemon processes
pkill -9 -f "daemon.js"

# 2. Clean up stale files
rm -rf ~/.agent-browser/*

# 3. Verify state file exists (if using --state)
ls -la /path/to/state.json

# 4. Try again with absolute path
agent-browser --headed --state /absolute/path/to/state.json open https://...
```

**Symptom:** `"--state ignored: daemon already running"`

**Cause:** The `--state` flag only works on the FIRST command when the daemon starts. If a daemon is already running, it ignores the flag.

**Fix:** Close the browser and kill the daemon first:
```bash
agent-browser close
pkill -9 -f "daemon.js"
rm -rf ~/.agent-browser/*
# Now --state will work on next command
```

## Skills & Resources

### Custom Skills

Custom Claude skills are installed in `.claude/skills/`:

| Skill | Description |
|-------|-------------|
| `agent-browser` | Web browsing automation (preferred for Semrush, Ahrefs, etc.) |
| `cherri-content-brief` | Generate SEO content briefs with Cherri brand voice |
| `cherri-returns-exchange` | Handle customer returns/exchanges via Shopify lookup |
| `cherri-shopify-seo` | Audit Shopify SEO (meta tags, schema, page speed) |
| `cherri-social-commerce` | Instagram/TikTok Shop optimization, ad performance |

### Third-Party Plugins

This project uses [wshobson/agents](https://github.com/wshobson/agents) for SEO plugins:

```bash
/plugin marketplace add wshobson/agents
/plugin install seo-content-creation@claude-code-workflows
/plugin install seo-technical-optimization@claude-code-workflows
/plugin install seo-analysis-monitoring@claude-code-workflows
/plugin install content-marketing@claude-code-workflows
```

### Context7 Library IDs

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

**Example:**
```
"How do I create an Instagram ad campaign? use context7"
"How do I list products in TikTok Shop? use context7"
```

## Development Standards

### Python

- **Package manager:** Use `uv` exclusively. Never use `pip`, `pip3`, or `pipx`.
  ```bash
  uv add <package>           # Add dependency to project
  uv tool install <package>  # Install CLI tool globally
  uvx <tool>                 # Run tool without installing
  ```
- **Type checking:** All Python code must be strongly typed. Use [ty](https://github.com/astral-sh/ty) (Astral's type checker) for validation.
- **Linting:** Use `ruff` with pedantic rule sets enabled. Check and fix before committing.
- **Type hints:** Use `from typing import Optional` for compatibility (not `X | None` union syntax which requires Python 3.10+).

### Scripts

Scripts in `bin/` should be executable with a shebang (`#!/usr/bin/env python3`) and follow the Python standards above.

## Project Files

### Conventions

- **Audits:** Files in `seo/audits/` must be date-prefixed: `YYYY-MM-DD-{topic}-audit.md`
- **Business documents:** Contracts, invoices, and vendor correspondence should be committed to the repo (in `vendors/documents/`). This is a private repo and these records are important to preserve.

### Vendors

Contractor and supplier relationships are tracked in `vendors/`. See `vendors/README.md` for structure and `vendors/index.yaml` for quick lookup.

### Financial Data

2025 financial records are in `financials/`. See `financials/README.md` for file reference and `financials/DATA_DICTIONARY.md` for schema documentation.

**2025 Key Metrics:**

| Metric | Value |
|--------|-------|
| Total Revenue | $205.2K (Shopify $166.6K + TikTok Shop $38.6K) |
| Total Ad Spend | $85.0K (Meta $77.4K + TikTok $7.7K) |
| Shopify Orders | 2,993 (avg $55.68/order) |
| Current Debt | $12.6K (Capital $4.3K + Credit $8.3K) |
| Best Month | Nov 2025: 570 orders, $25K revenue |
| Worst Month | May 2025: 45 orders, $3K revenue |

### Shopify Theme

The live Shopify theme (Palo Alto) is downloaded to `theme/`. This is a full snapshot of all theme files: Liquid templates, sections, snippets, assets, config, and locales.

**Re-download:** Run `bin/download-theme` to pull a fresh copy from the live theme. Requires a valid Shopify access token (run `bin/refresh-shopify-token` first if expired).

**Structure:** `assets/`, `config/`, `layout/`, `locales/`, `sections/`, `snippets/`, `templates/`
