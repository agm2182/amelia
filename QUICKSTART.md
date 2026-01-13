# Quickstart Guide

Get set up with the Cherri SEO research environment in 5 minutes.

## Prerequisites

- [Claude Code](https://claude.com/code) installed
- Access to Cherri's Shopify admin (for making changes)
- Google account with access to Cherri's GSC/GA4 (for analytics)

## Step 1: Clone and Open

```bash
git clone https://github.com/gabyscaringe/cherri.git
cd cherri
claude
```

## Step 2: Install SEO Plugins

When you first open the project, you'll be prompted to install the wshobson/agents marketplace. Accept it, then install the SEO plugins:

```
/plugin install seo-content-creation
/plugin install seo-technical-optimization
/plugin install seo-analysis-monitoring
/plugin install content-marketing
```

These provide:
- **seo-content-creation** - E-E-A-T optimized content writing
- **seo-technical-optimization** - Meta tags, schema, featured snippets
- **seo-analysis-monitoring** - Freshness and cannibalization detection
- **content-marketing** - Research and strategy workflows

## Step 3: Configure Google APIs (One-time)

If you need access to GSC/GA4 data, get the credentials file from the team lead and save it to:

```
~/.config/cherri/cherri-seo-credentials.json
```

The MCP servers are already configured in `.claude.json` and will use this file automatically.

**Already configured:**
- Google Search Console (property: `sc-domain:shopcherri.com`)
- Google Analytics 4 (property ID: `386275004`)

## Step 4: Verify Setup

Test that everything works:

```
"Show me the top organic landing pages from GA4 for the last 7 days"
```

You should see data from the Cherri GA4 property.

## What's Available

### MCP Data Sources
| Source | What it provides |
|--------|------------------|
| Google Search Console | Search queries, impressions, clicks, positions |
| Google Analytics 4 | Traffic, conversions, user behavior |
| Shopify Dev | API documentation, GraphQL schema reference |
| Context7 | Up-to-date library documentation |

### Custom Skills (in `skills/`)
| Skill | Purpose |
|-------|---------|
| `cherri-keyword-research` | Find keyword opportunities |
| `cherri-competitor-analysis` | Track competitor SEO |
| `cherri-shopify-seo` | Audit storefront SEO |
| `cherri-content-brief` | Generate content briefs |

### Research Outputs
All research goes in `research/`:
- `audits/` - SEO audit reports
- `keywords/` - Keyword research
- `competitors/` - Competitor analysis
- `content-briefs/` - Content planning

## Common Tasks

**Run an SEO audit:**
```
"Audit the current SEO status using GSC and GA4 data"
```

**Find keyword opportunities:**
```
"Find striking distance keywords (positions 4-20) with high impressions"
```

**Generate a content brief:**
```
"Create a content brief for 'best underwear for working out'"
```

**Check indexing status:**
```
"Check if shopcherri.com/collections/panties is indexed"
```

## Troubleshooting

**"No data from GSC/GA4"**
- Check that `~/.config/cherri/cherri-seo-credentials.json` exists
- Verify the service account has access to the properties

**"Plugin not found"**
- Run `/plugin` to see available plugins
- Re-run `/plugin install <name>` if needed

**"MCP server error"**
- Check that Node.js is installed
- Try restarting Claude Code

## Next Steps

1. Review `research/action-items.md` for current priorities
2. Check `research/audits/` for the latest SEO audit
3. Read `CLAUDE.md` for detailed tool documentation
