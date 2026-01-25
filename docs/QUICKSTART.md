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

First, add the wshobson/agents marketplace (registered as `claude-code-workflows`):

```
/plugin marketplace add wshobson/agents
```

Then install the SEO plugins:

```
/plugin install seo-content-creation@claude-code-workflows
/plugin install seo-technical-optimization@claude-code-workflows
/plugin install seo-analysis-monitoring@claude-code-workflows
/plugin install content-marketing@claude-code-workflows
```

These provide:
- **seo-content-creation** - E-E-A-T optimized content writing
- **seo-technical-optimization** - Meta tags, schema, featured snippets
- **seo-analysis-monitoring** - Freshness and cannibalization detection
- **content-marketing** - Research and strategy workflows

## Step 3: Configure Google APIs (One-time)

Get the credentials file from the team lead and save it to:

```
~/.config/cherri/cherri-seo-credentials.json
```

The MCP servers are already configured in `.claude.json` and will use this file automatically.

**Properties already configured:**
- Google Search Console: `sc-domain:shopcherri.com`
- Google Analytics 4: `386275004`

**File locations:**
- Credentials: `~/.config/cherri/` (outside git repo)
- Raw data exports: `data/` (gitignored)
- Research outputs: `research/` subdirectories

## Step 4: Verify Setup

Run the integration check script:

```bash
bin/check-integrations
```

This tests all configured APIs (GSC, GA4, Meta Ads, TikTok Ads, Shopify) and reports which are working.

You can also test interactively:

```
"Show me the top organic landing pages from GA4 for the last 7 days"
```

You should see data from the Cherri GA4 property.

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

See the [README](README.md) for common tasks and current priorities.
