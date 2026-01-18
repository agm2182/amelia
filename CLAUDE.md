# Cherri SEO Research - Project Notes

## Project Context

SEO and growth research for Cherri, an underwear e-commerce company on Shopify.

## Tool Status

Run `bin/check-integrations` to verify API credentials are working.

> **Note:** `bin/check-integrations` tests API credentials directly via curl, not MCP servers. MCP servers may fail even if credentials work (e.g., wrong package name).

| Tool | Status | Package | Notes |
|------|--------|---------|-------|
| Google Search Console | Ready | `mcp-server-gsc` (npm) | Uses `GOOGLE_APPLICATION_CREDENTIALS` |
| Google Analytics 4 | Ready | `analytics-mcp` (uvx, official Google) | Uses `GOOGLE_APPLICATION_CREDENTIALS` + `GOOGLE_PROJECT_ID` |
| Gmail | Ready | `@gongrzhe/server-gmail-autoauth-mcp` | OAuth tokens in `~/.gmail-mcp/credentials.json` |
| Meta Ads | Ready | `meta-ads-mcp` (npm) | Uses `META_ACCESS_TOKEN` from `.env` |
| TikTok Ads | Ready | `tiktok-ads-mcp` (uvx) | Uses `TIKTOK_ACCESS_TOKEN`, `TIKTOK_ADVERTISER_IDS` from `.env` |
| Shopify Dev MCP | Ready | N/A | No auth needed. Use for API docs and GraphQL schema. |
| Shopify Admin API | Ready | `@ajackus/shopify-mcp-server` (npm) | Token in `~/.config/cherri/shopify-credentials.json` |
| Canva | Ready | `mcp-remote` → `https://mcp.canva.com/mcp` | Browser OAuth on first use |
| Semrush | No API | N/A | Start plan lacks API. Use Chrome MCP. |
| Ahrefs | No API | N/A | Free account. Use Chrome MCP. |
| Chrome MCP | Ready | `claude-in-chrome` | Use for web-based research when APIs unavailable |

**MCP Configuration:** See `.mcp.json` for server definitions. Credentials stored in `~/.config/cherri/`.

## Python Environment

Python is managed via [uv](https://docs.astral.sh/uv/) (installed at `~/.local/bin/uv`).

```bash
# List installed Python versions
uv python list --only-installed

# Install a new Python version
uv python install 3.13

# Run a Python package (like pipx run)
uvx --python 3.13 <package>
```

The GA4 MCP uses `uvx --python 3.13 analytics-mcp`.

## Token Refresh

### TikTok Access Token

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

### Meta Access Token

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

## Instagram Graph API (Direct Usage)

The Meta Ads MCP doesn't cover Instagram comment management. Use the Graph API directly with curl.

**Account IDs:**
- Instagram Account: `17841403097399699` (@shopcherri)
- Facebook Page: `773863439614388` (Cherri)
- Business ID: `1174640472693824`

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

### Shopify Access Token

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

## Workarounds

### Semrush (No API Access)

Use Chrome MCP to browse Semrush web interface.

**Key URLs:**
- Keyword Overview: https://www.semrush.com/analytics/keywordoverview/
- Domain Overview: https://www.semrush.com/analytics/overview/
- Keyword Magic Tool: https://www.semrush.com/analytics/keywordmagic/
- Position Tracking: https://www.semrush.com/position-tracking/

### Ahrefs (Free Account, No API)

Use Chrome MCP to browse Ahrefs web interface.

**Key URLs:**
- Site Explorer: https://app.ahrefs.com/site-explorer
- Keywords Explorer: https://app.ahrefs.com/keywords-explorer
- Content Explorer: https://app.ahrefs.com/content-explorer
- Rank Tracker: https://app.ahrefs.com/rank-tracker

### Google Ads (Web UI)

Use Chrome MCP to browse Google Ads interface.

**Key URLs:**
- Keyword Planner: https://ads.google.com/aw/keywordplanner/home
- Campaign Dashboard: https://ads.google.com/aw/campaigns
- Performance Reports: https://ads.google.com/aw/reporting/reporteditor

### Shopify Admin (Web UI)

Use Chrome MCP for visual tasks or when API doesn't expose needed data.

**Key URLs:**
- Products: https://admin.shopify.com/store/shop-cherri/products
- Pages: https://admin.shopify.com/store/shop-cherri/pages
- Blog Posts: https://admin.shopify.com/store/shop-cherri/articles
- Navigation: https://admin.shopify.com/store/shop-cherri/menus
- Themes: https://admin.shopify.com/store/shop-cherri/themes

## Skills

Custom Claude skills are installed in `.claude/skills/`:

| Skill | Description |
|-------|-------------|
| `cherri-content-brief` | Generate SEO content briefs with Cherri brand voice |
| `cherri-shopify-seo` | Audit Shopify SEO (meta tags, schema, page speed) |
| `cherri-social-commerce` | Instagram/TikTok Shop optimization, ad performance |

Skills requiring additional setup are documented in `skills/README.md`.

## Third-Party Plugins

This project uses [wshobson/agents](https://github.com/wshobson/agents) for SEO plugins. See [QUICKSTART.md](QUICKSTART.md) for installation.

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

**Example:**
```
"How do I create an Instagram ad campaign? use context7"
"How do I list products in TikTok Shop? use context7"
```

## Cherri Info

- **Domain:** shopcherri.com
- **Myshopify domain:** shop-cherri.myshopify.com
- **GSC Property:** sc-domain:shopcherri.com
- **GA4 Property ID:** 386275004
- **Meta Ad Account ID:** act_2026819017404527
- **TikTok App ID:** 7595068986274938881
- **TikTok Advertiser IDs:** 6872850369307738114, 6872851292415328257
- **Competitor Intel:** See `research/competitors.md` for detailed competitive analysis
