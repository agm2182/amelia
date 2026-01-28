# Cherri

Claude Code-powered business operations for [Cherri](https://shopcherri.com), an underwear e-commerce company.

## Quick Start

```bash
git clone https://github.com/gabyscaringe/cherri.git
cd cherri
claude
```

See **[CLAUDE.md](CLAUDE.md)** for detailed tool documentation and setup.

## What This Does

- **E-commerce Operations** - Shopify admin, orders, inventory, returns
- **Paid Advertising** - Meta and TikTok ad campaigns, performance reports
- **Marketing & SEO** - Audits, keyword research, content briefs
- **Financial Tracking** - Revenue, expenses, ad spend, loans
- **Customer Research** - Surveys, psychographics, competitor analysis
- **Content & Design** - Copywriting, social content, Canva

## Integrations

| Service | Purpose |
|---------|---------|
| Shopify Admin | Products, orders, inventory, customers |
| Meta Ads | Facebook/Instagram campaigns |
| TikTok Ads | TikTok campaigns |
| Google Analytics 4 | Traffic and conversions |
| Google Search Console | SEO and indexing |
| Canva | Design assets |
| Gmail | Customer communication |

## Project Structure

```
.claude/skills/        # Active Claude skills
.claude/draft-skills/  # Skills in development
brand/                 # Brand identity, voice, surveys
competitors/           # Competitor deep-dives and analysis
financials/            # 2025 financial records
marketing/             # Content briefs, plans, strategy
operations/            # Policies (returns, etc.)
seo/                   # Audits and schema markup
CLAUDE.md              # Tool documentation and setup
```

## Custom Skills

| Skill | Description |
|-------|-------------|
| `cherri-returns-exchange` | Handle customer returns via Shopify |
| `cherri-shopify-seo` | Audit Shopify SEO and schema |
| `cherri-social-commerce` | Instagram/TikTok Shop optimization |
| `cherri-content-brief` | Generate SEO content briefs |
| `paid-ads` | Ad campaign management |
| `copywriting` | Marketing copy generation |

## Common Tasks

Example prompts for common operations:

### SEO & Search

```
"Audit the current SEO status using GSC and GA4 data"
"Find striking distance keywords (positions 4-20) with high impressions"
"Check if shopcherri.com/collections/panties is indexed"
"Show pages with high impressions but low CTR"
```

### Analytics

```
"Show top organic landing pages from GA4 for the last 30 days"
"Compare this month's traffic to last month"
"What's the conversion rate by traffic source?"
```

### Content

```
"Create a content brief for 'best underwear for working out'"
"Write product descriptions for the new thong collection"
"Generate social captions for a holiday sale"
```

### Shopify

```
"Look up order #12345"
"Check inventory levels for the cheeky style"
"Find customers who ordered in the last 7 days"
```

### Advertising

```
"Show Meta ad performance for the last 30 days"
"Compare ROAS across active TikTok campaigns"
"What's our cost per acquisition this month?"
```

### Customer Service

```
"Process exchange for order #12345 - customer wants size M instead of S"
"Draft a response for a customer asking about returns"
```

## Current Status

- **Domain:** shopcherri.com
- **2025 Revenue:** $205K (Shopify $167K + TikTok Shop $39K)
- **2025 Ad Spend:** $85K (Meta $77K + TikTok $8K)

See `financials/` for detailed records and `seo/audits/` for findings.
