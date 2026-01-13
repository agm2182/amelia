# Cherri SEO & Growth Research

Claude Code-powered SEO research infrastructure for [Cherri](https://shopcherri.com), an underwear e-commerce company.

## Quick Start

```bash
git clone https://github.com/gabyscaringe/cherri.git
cd cherri
claude
```

See **[QUICKSTART.md](QUICKSTART.md)** for full setup instructions.

## What This Does

- **SEO Audits** - Analyze site health, indexing, and technical issues
- **Keyword Research** - Find opportunities from GSC and competitor data
- **Content Planning** - Generate briefs for blog posts and landing pages
- **Performance Tracking** - Monitor organic traffic and conversions

## Data Sources

| Source | Access |
|--------|--------|
| Google Search Console | Via MCP (configured) |
| Google Analytics 4 | Via MCP (configured) |
| Semrush | Via Chrome (Start plan) |
| Ahrefs | Via Chrome (Free account) |
| Shopify Admin | Via Chrome |

## Project Structure

```
research/          # All research outputs
  ├── audits/      # SEO audit reports
  ├── action-items.md  # Running TODO list
skills/            # Custom Claude skills
.claude/           # Plugin configuration
CLAUDE.md          # Detailed tool documentation
```

## Current Status

- **Domain:** shopcherri.com
- **GSC Property:** sc-domain:shopcherri.com
- **GA4 Property:** 386275004
- **Organic Revenue:** ~$4k/month (baseline Jan 2026)

See `research/audits/` for latest findings and `research/action-items.md` for priorities.
