# Cherri SEO Research - Project Notes

## Project Context

SEO and growth research for Cherri, an underwear e-commerce company on Shopify.

## Tool Status

| Tool | Status | Notes |
|------|--------|-------|
| Google Search Console | Ready | MCP configured in `.mcp.json` |
| Google Analytics 4 | Ready | MCP configured in `.mcp.json` |
| Meta Ads MCP | Ready | Credentials in `~/.config/cherri/.env` |
| TikTok Ads MCP | Setup needed | Configured in `.mcp.json`, needs access token |
| Shopify Dev MCP | Ready | No auth needed. Use for API docs and GraphQL schema. |
| Shopify Admin API | Setup needed | Needs Custom App token. See `skills/README.md` |
| Semrush | API blocked | Start plan lacks API. Use Chrome MCP. |
| Ahrefs | Free account | No API access. Use Chrome MCP. |
| Chrome MCP | Ready | Use for web-based research when APIs unavailable |

**MCP Configuration:** See `.mcp.json` for server definitions. Credentials stored in `~/.config/cherri/`.

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

Use Chrome MCP until API access is resolved.

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
- **Primary competitors:** Parade, Tommy John, MeUndies, Cuup, ThirdLove
