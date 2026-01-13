# Cherri SEO Research - Project Notes

## Project Context
SEO and growth research for Cherri, an underwear e-commerce company on Shopify.

## Tool Status

| Tool | Status | Notes |
|------|--------|-------|
| Semrush MCP | API blocked | Start plan lacks API access. Use Chrome MCP to access web UI instead. |
| Shopify Dev MCP | Ready | No auth needed. Use for API docs and GraphQL schema. |
| Shopify Admin API | Blocked | Client credentials grant not working - see notes below |
| Google Search Console | Ready | MCP configured with service account |
| Google Analytics 4 | Ready | MCP configured with service account |
| Google Ads | Access granted | No MCP yet - use web UI via Chrome |
| Ahrefs | Free account | No API access. Use Chrome MCP to access web UI (already logged in). |
| Chrome MCP | Ready | Use for web-based research when APIs unavailable |

## Workarounds

### Semrush (No API Access)
Use Chrome MCP to browse Semrush web interface:
1. Navigate to semrush.com and log in
2. Run keyword research, competitor analysis via web UI
3. Export data or screenshot results as needed

**Key Semrush URLs:**
- Keyword Overview: https://www.semrush.com/analytics/keywordoverview/
- Domain Overview: https://www.semrush.com/analytics/overview/
- Keyword Magic Tool: https://www.semrush.com/analytics/keywordmagic/
- Position Tracking: https://www.semrush.com/position-tracking/

**Docs:** https://www.semrush.com/kb/

### Ahrefs (Free Account, No API)
Use Chrome MCP to browse Ahrefs web interface (already logged in):
1. Navigate to ahrefs.com
2. Use Site Explorer, Keywords Explorer, etc. via web UI
3. Free account has limited searches - use strategically

**Key Ahrefs URLs:**
- Site Explorer: https://app.ahrefs.com/site-explorer
- Keywords Explorer: https://app.ahrefs.com/keywords-explorer
- Content Explorer: https://app.ahrefs.com/content-explorer
- Rank Tracker: https://app.ahrefs.com/rank-tracker

**Docs:** https://help.ahrefs.com/

### Google Ads (Web UI)
Use Chrome MCP to browse Google Ads interface:

**Key Google Ads URLs:**
- Keyword Planner: https://ads.google.com/aw/keywordplanner/home
- Campaign Dashboard: https://ads.google.com/aw/campaigns
- Performance Reports: https://ads.google.com/aw/reporting/reporteditor

**Docs:** https://support.google.com/google-ads/

### Shopify Admin (Web UI Fallback)
Until API access is resolved, use Chrome MCP:

**Key Shopify Admin URLs:**
- Products: https://admin.shopify.com/store/shop-cherri/products
- Pages: https://admin.shopify.com/store/shop-cherri/pages
- Blog Posts: https://admin.shopify.com/store/shop-cherri/articles
- Navigation: https://admin.shopify.com/store/shop-cherri/menus
- Themes: https://admin.shopify.com/store/shop-cherri/themes

**Docs:** https://help.shopify.com/en/manual

### Data Storage
- Raw exports go in `data/` (gitignored)
- Research outputs go in `research/` subdirectories
- Content briefs go in `research/content-briefs/`

### Credentials Storage
All credentials stored in `~/.config/cherri/` (outside git repo):
- `cherri-seo-credentials.json` - GCP service account for GSC/GA4
- `shopify-credentials.json` - Shopify API client ID/secret

## Custom Skills
Located in `skills/`:
- `cherri-keyword-research` - Keyword opportunity discovery
- `cherri-competitor-analysis` - Competitive intelligence
- `cherri-shopify-seo` - Storefront SEO audits
- `cherri-content-brief` - Content brief generation

## Third-Party Plugins/Skills to Explore

From ChatGPT research - not yet installed or verified:

### wshobson/agents (Verified exists)
```bash
/plugin marketplace add wshobson/agents
/plugin install seo-content-creation
/plugin install seo-technical-optimization
/plugin install seo-analysis-monitoring
/plugin install content-marketing
```
- SEO content writing/planning + quality auditing
- Meta tags, schema, structure, featured snippets
- Freshness/cannibalization/authority analysis
- Strategy + web research + synthesis

**Docs:** https://github.com/wshobson/agents

### alirezarezvani/claude-skills (Unverified)
```bash
npx ai-agent-skills install alirezarezvani/claude-skills --agent claude
```
- Content Creator with SEO optimizer
- Social Media Analyzer (multi-platform)
- Instagram + TikTok optimization guides

**Claimed repo:** https://github.com/alirezarezvani/claude-skills

### henkisdabro/wookstar-claude-plugins (Unverified)
```bash
/plugin marketplace add henkisdabro/wookstar-claude-plugins
/plugin install marketing@wookstar
/plugin install shopify-developer@wookstar
```
- GTM + GA4 + Google Ads Scripts
- Shopify development bundle

**Claimed repo:** https://github.com/henkisdabro/claudecode-marketplace

### jeffallan/claude-skills (Unverified)
```bash
/plugin marketplace add jeffallan/claude-skills
/plugin install fullstack-dev-skills@jeffallan
```
- Shopify Expert skill
- Platform specialist skills

**Claimed repo:** https://github.com/Jeffallan/claude-skills

### m2ai-portfolio/claude-skills (Unverified)
- Instagram Caption Generator
- Blog Post Outline Creator (SEO-optimized)
- Meta Description Generator
- Product Description Writer

**Claimed repo:** https://github.com/m2ai-portfolio/claude-skills

### kudosx/claude-skill-browser-use (Unverified)
- TikTok trend scanning
- Browser automation for social platforms

**Claimed repo:** https://github.com/kudosx/claude-skill-browser-use

**Note:** "Unverified" means the repo couldn't be confirmed to exist when checked. Try installing and see if they work.

## Context7 Library IDs

Use these with `use context7` for up-to-date documentation:

| Library | Context7 ID | Snippets | Score |
|---------|-------------|----------|-------|
| Shopify Developer Docs | `/websites/shopify_dev` | 53,258 | 67.7 |
| Shopify GraphQL Admin API | `/websites/shopify_dev_api_admin-graphql_2025-07` | 12,376 | 36.4 |
| GA4 Data API v1 | `/websites/developers_google_analytics_devguides_reporting_data_v1` | 7,196 | 79.1 |
| Google Search Console API | `/websites/developers_google_webmaster-tools` | 1,718 | 61.0 |
| Google Ads API | `/websites/developers_google_google-ads_api` | 54,803 | 71.3 |

**Example usage:**
```
"How do I update product SEO fields in Shopify GraphQL? use context7"
"Show GA4 Data API examples for custom reports. use context7"
```

## Cherri Info
- **Domain:** shopcherri.com
- **Myshopify domain:** shop-cherri.myshopify.com
- **GSC Property:** sc-domain:shopcherri.com
- **GA4 Property ID:** 386275004
- **Primary competitors:** Parade, Tommy John, MeUndies, Cuup, ThirdLove
- **Target market:** (add when known)

## Research Priorities
1. Technical SEO audit
2. Keyword research + content opportunities
3. Competitor analysis
4. Content brief creation

## Notes

### 2025-01-13: Initial GSC Check
- GSC connection working ✓
- No search analytics data for last 30 days (low/no organic traffic yet)
- Sitemap submitted ✓ - no errors, no warnings

### 2025-01-13: GA4 Setup Complete
- GA4 connection working ✓
- Property: shopcherri - GA4 (386275004)
- Traffic: ~1,300-1,700 sessions/day
- Note: Traffic exists but no organic search data in GSC = likely paid/social/direct traffic

### 2025-01-13: Shopify API Setup (Incomplete)
**Problem:** Client credentials grant returns "shop_not_permitted" error.

**What we tried:**
1. Created app in Shopify Partners Dev Dashboard (new method as of Jan 2026)
2. Configured scopes: read_products, read_content, read_themes, read_metaobjects, read_online_store_pages
3. Installed app to store
4. Got Client ID and Secret
5. Client credentials grant failed - store not linked to Partner account

**Blocker:** Partner account email same as store owner email, can't add as managed store.

**Credentials saved:** `~/.config/cherri/shopify-credentials.json`
- Client ID: fd3abae1194aa0e0e35d850fecc536ab
- Client Secret: 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
- Domain: shop-cherri.myshopify.com

**Next steps to try:**
1. Check Shopify Admin → Settings → Apps → Develop apps for direct access
2. Try authorization code grant flow instead of client credentials
3. Or use Shopify CLI for authentication
4. Fallback: Use Chrome MCP to access Shopify Admin manually
