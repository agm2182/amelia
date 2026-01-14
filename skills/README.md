# Skills Requiring Additional Setup

These skills are not installed because they require API access that isn't currently available.

## cherri-shopify-seo-api

**What it does:** Full Shopify SEO management - audit AND apply changes via GraphQL API

**Current blockers:**

| Dependency | Required For | Status | How to Fix |
|------------|--------------|--------|------------|
| Shopify Admin API token | Read/write products, collections, pages | Blocked - client credentials not working | Create private app or custom app |

**What works without this:** The installed `cherri-shopify-seo` skill can audit via Chrome MCP, but changes must be applied manually in Shopify Admin.

**To enable this skill:**

1. Create a Custom App in Shopify Admin:
   - Go to Settings > Apps and sales channels > Develop apps
   - Create app, configure Admin API scopes:
     - `read_products`, `write_products`
     - `read_content`, `write_content`
     - `read_online_store_pages`, `write_online_store_pages`
   - Install app and get Admin API access token

2. Store credentials securely:
   ```bash
   # Add to ~/.config/cherri/.env (gitignored)
   SHOPIFY_STORE=shop-cherri.myshopify.com
   SHOPIFY_ACCESS_TOKEN=shpat_xxxxx
   ```

3. Add Shopify MCP server to `.claude.json`:
   ```json
   {
     "mcpServers": {
       "shopify-admin": {
         "command": "npx",
         "args": ["@anthropic/shopify-admin-mcp"],
         "env": {
           "SHOPIFY_STORE": "${SHOPIFY_STORE}",
           "SHOPIFY_ACCESS_TOKEN": "${SHOPIFY_ACCESS_TOKEN}"
         }
       }
     }
   }
   ```

   **Note:** Check if `@anthropic/shopify-admin-mcp` exists, otherwise use a community MCP or direct GraphQL calls.

4. Move skill to `.claude/skills/cherri-shopify-seo-api/SKILL.md`

---

## cherri-social-commerce

**What it does:** Optimize Instagram Shop and TikTok Shop - catalog health, ad performance, traffic driving

**Current blockers:**

| Dependency | Required For | Status | How to Fix |
|------------|--------------|--------|------------|
| Shopify API | Product optimization (syncs to both platforms) | Blocked | Create Custom App (free) |
| Meta Ads MCP | Instagram ad analytics, campaigns | Working | Configured in `~/.config/cherri/.env` |
| TikTok Ads MCP | TikTok ad analytics, campaigns | Blocked | Get TikTok Business API token |
| Chrome MCP | Shop management fallback | Working | Already configured |

**What works without full setup:** Chrome MCP can access Commerce Manager and Seller Center for manual management.

**To enable this skill:**

1. Set up Shopify API (see cherri-shopify-seo-api above)

2. Get Meta Business access token:
   - Go to https://developers.facebook.com
   - Create app or use existing
   - Add "Marketing API" product
   - Generate access token with `ads_read` permission
   - Get Ad Account ID from Business Manager

3. Get TikTok Business API token:
   - Go to https://business-api.tiktok.com
   - Create developer account
   - Create app with Marketing API access
   - Get access token and Advertiser ID

4. Store credentials:
   ```bash
   # Add to ~/.config/cherri/.env
   META_ACCESS_TOKEN=your_meta_token
   META_AD_ACCOUNT_ID=act_123456789
   TIKTOK_ACCESS_TOKEN=your_tiktok_token
   TIKTOK_ADVERTISER_ID=123456789
   ```

5. Move skill to `.claude/skills/cherri-social-commerce/SKILL.md`

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

| Service | Current Plan | Required Plan | Monthly Cost |
|---------|--------------|---------------|--------------|
| Shopify Admin API | N/A | Custom App (free) | $0 |
| Meta Ads API | ✓ Configured | Business account (free) | $0 |
| TikTok Ads API | N/A | Business account (free) | $0 |
| Semrush | Start ($0) | Guru | $129 |
| Ahrefs | Free ($0) | Lite | $129 |
| **Total** | **$0** | | **$258/mo** |

**Free to set up:** Shopify and TikTok Ads APIs just require developer account setup (no paid plans needed). Meta Ads API is already configured.

## Alternative: Chrome MCP Workflows

Instead of API access, you can use the skill workflows as **manual checklists** with Chrome MCP:

1. Read the skill file for the workflow steps
2. Use Chrome MCP to navigate to Semrush/Ahrefs web UI
3. Manually extract the data points listed in each step
4. Record results in the specified output files

This is slower but works with current free/low-tier accounts.

## Installed Skills

These skills are installed and working in `.claude/skills/`:

| Skill | Description |
|-------|-------------|
| `cherri-content-brief` | Generate SEO content briefs with brand voice |
| `cherri-shopify-seo` | Audit Shopify SEO via Chrome MCP (read-only) |
| `cherri-social-commerce` | Instagram/TikTok Shop + ad performance (Meta Ads ready, TikTok pending) |

## Skills Pending Setup

| Skill | Blocker | Effort |
|-------|---------|--------|
| `cherri-shopify-seo-api` | Create Shopify Custom App | 15 min, free |
| `cherri-keyword-research` | Semrush Guru plan | $129/mo |
| `cherri-competitor-analysis` | Ahrefs + Semrush | $258/mo |

## Priority Setup Order

1. **Shopify API** (15 min) - Unlocks `cherri-shopify-seo-api`, enables product sync
2. ~~**Meta Ads API**~~ ✓ Done - Configured in `~/.config/cherri/.env`
3. **TikTok Ads API** (10 min) - Unlocks TikTok ads analytics
4. After 1-3: `cherri-social-commerce` is fully functional
