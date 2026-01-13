# Cherri SEO Research - Project Notes

## Project Context

SEO and growth research for Cherri, an underwear e-commerce company on Shopify.

## Tool Status

| Tool | Status | Notes |
|------|--------|-------|
| Semrush MCP | API blocked | Start plan lacks API access. Use Chrome MCP instead. |
| Shopify Dev MCP | Ready | No auth needed. Use for API docs and GraphQL schema. |
| Shopify Admin API | Blocked | Client credentials grant not working. Use Chrome MCP. |
| Google Search Console | Ready | MCP configured with service account |
| Google Analytics 4 | Ready | MCP configured with service account |
| Google Ads | Access granted | No MCP yet - use Chrome MCP |
| Ahrefs | Free account | No API access. Use Chrome MCP. |
| Chrome MCP | Ready | Use for web-based research when APIs unavailable |

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

## Third-Party Plugins

This project uses [wshobson/agents](https://github.com/wshobson/agents) for SEO plugins. See [QUICKSTART.md](QUICKSTART.md) for installation.

## Context7 Library IDs

Use these with `use context7` for up-to-date documentation:

| Library | Context7 ID |
|---------|-------------|
| Shopify Developer Docs | `/websites/shopify_dev` |
| Shopify GraphQL Admin API | `/websites/shopify_dev_api_admin-graphql_2025-07` |
| GA4 Data API v1 | `/websites/developers_google_analytics_devguides_reporting_data_v1` |
| Google Search Console API | `/websites/developers_google_webmaster-tools` |
| Google Ads API | `/websites/developers_google_google-ads_api` |

**Example:**
```
"How do I update product SEO fields in Shopify GraphQL? use context7"
```

## Cherri Info

- **Domain:** shopcherri.com
- **Myshopify domain:** shop-cherri.myshopify.com
- **GSC Property:** sc-domain:shopcherri.com
- **GA4 Property ID:** 386275004
- **Primary competitors:** Parade, Tommy John, MeUndies, Cuup, ThirdLove
