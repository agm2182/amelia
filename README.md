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
research/              # All research outputs
  ├── audits/          # SEO audit reports
  ├── keywords/        # Keyword research exports
  ├── competitors/     # Competitor analysis
  ├── content-briefs/  # Content brief documents
  └── action-items.md  # Running TODO list
.claude/
  ├── skills/          # Installed Claude skills
  └── settings.json    # Plugin configuration
skills/                # Skills requiring setup (see README)
CLAUDE.md              # Detailed tool documentation
```

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

**Analyze traffic:**
```
"Show top organic landing pages from GA4 for the last 30 days"
```

## Current Status

- **Domain:** shopcherri.com
- **GSC Property:** sc-domain:shopcherri.com
- **GA4 Property:** 386275004
- **Organic Revenue:** ~$4k/month (baseline Jan 2026)

See `research/audits/` for latest findings and `research/action-items.md` for priorities.
