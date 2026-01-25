# Skills Setup Status

Overview of skill dependencies and setup requirements.

## cherri-shopify-seo-api

**What it does:** Full Shopify SEO management - audit AND apply changes via GraphQL API

**Status: ✅ Ready**

| Dependency | Required For | Status |
|------------|--------------|--------|
| Shopify Admin API token | Read/write products, collections, pages | ✅ Configured |

**Configuration:**
- MCP server: `@ajackus/shopify-mcp-server` (configured in `.mcp.json`)
- Credentials: `~/.config/cherri/shopify-credentials.json`
- Token refresh: Run `bin/refresh-shopify-token` (tokens expire every 24h)

---

## cherri-social-commerce

**What it does:** Optimize Instagram Shop and TikTok Shop - catalog health, ad performance, traffic driving

**Status: ✅ Ready**

| Dependency | Required For | Status |
|------------|--------------|--------|
| Shopify API | Product optimization (syncs to both platforms) | ✅ Configured |
| Meta Ads MCP | Instagram ad analytics, campaigns | ✅ Configured |
| TikTok Ads MCP | TikTok ad analytics, campaigns | ✅ Configured |
| Chrome MCP | Shop management fallback | ✅ Configured |

**Configuration:**
- Meta Ads: `~/.config/cherri/.env` (META_ACCESS_TOKEN, META_AD_ACCOUNT_ID)
- TikTok Ads: `~/.config/cherri/.env` (TIKTOK_ACCESS_TOKEN, TIKTOK_ADVERTISER_IDS)
- Shopify: `~/.config/cherri/shopify-credentials.json`

---

## cherri-keyword-research

**What it does:** Striking distance audits, keyword discovery, competitor gap analysis

**Current blockers:**

| Dependency | Required For | Status | How to Fix |
|------------|--------------|--------|------------|
| Semrush API | Search volume, keyword difficulty, competitor rankings | Blocked - Start plan lacks API | Upgrade to Guru+ plan ($129/mo) |
| GSC MCP | Current rankings, impressions, CTR | Working | Already configured |

**Workaround available:** Use Chrome MCP to browse Semrush web UI manually:
- Keyword Overview: https://www.semrush.com/analytics/keywordoverview/
- Keyword Magic Tool: https://www.semrush.com/analytics/keywordmagic/

**To enable this skill:**
1. Upgrade Semrush to Guru plan or higher
2. Get API key from Semrush settings
3. Add Semrush MCP server to `.claude.json`:
```json
{
  "mcpServers": {
    "semrush": {
      "command": "npx",
      "args": ["@anthropic/semrush-mcp"],
      "env": {
        "SEMRUSH_API_KEY": "<your-key>"
      }
    }
  }
}
```
4. Move `skills/cherri-keyword-research/SKILL.md` to `.claude/skills/cherri-keyword-research/SKILL.md`

---

## cherri-competitor-analysis

**What it does:** Ranking comparisons, content gaps, backlink analysis

**Current blockers:**

| Dependency | Required For | Status | How to Fix |
|------------|--------------|--------|------------|
| Ahrefs API | Backlink data, referring domains, DR scores | Blocked - Free account | Upgrade to Lite+ plan ($129/mo) |
| Semrush API | Competitor organic keywords | Blocked - Start plan | Upgrade to Guru+ plan |
| GSC MCP | Cherri's own rankings | Working | Already configured |

**Workaround available:** Use Chrome MCP to browse Ahrefs/Semrush web UIs:
- Ahrefs Site Explorer: https://app.ahrefs.com/site-explorer
- Semrush Domain Overview: https://www.semrush.com/analytics/overview/

**To enable this skill:**
1. Upgrade Ahrefs to Lite plan or higher
2. Get API key from Ahrefs dashboard
3. Add Ahrefs MCP server (if one exists) or create custom integration
4. Also requires Semrush API (see above)
5. Move skill to `.claude/skills/cherri-competitor-analysis/SKILL.md`

---

## Cost Summary

To fully enable all skills:

| Service | Status | Monthly Cost |
|---------|--------|--------------|
| Shopify Admin API | ✅ Configured | $0 |
| Meta Ads API | ✅ Configured | $0 |
| TikTok Ads API | ✅ Configured | $0 |
| Semrush API | ❌ Requires Guru plan | $129 |
| Ahrefs API | ❌ Requires Lite plan | $129 |

## Alternative: Chrome MCP Workflows

For Semrush and Ahrefs (no API access), use Chrome MCP to browse web UIs manually:

1. Read the skill file for the workflow steps
2. Use Chrome MCP to navigate to Semrush/Ahrefs web UI
3. Manually extract the data points listed in each step
4. Record results in the specified output files

## Installed Skills

These skills are installed and working in `.claude/skills/`:

| Skill | Description |
|-------|-------------|
| `cherri-content-brief` | Generate SEO content briefs with brand voice |
| `cherri-shopify-seo` | Full Shopify SEO management via Admin API |
| `cherri-social-commerce` | Instagram/TikTok Shop + ad performance |

## Skills Pending Setup

| Skill | Blocker | Effort |
|-------|---------|--------|
| `cherri-keyword-research` | Semrush Guru plan | $129/mo |
| `cherri-competitor-analysis` | Ahrefs + Semrush | $258/mo |
