---
name: cherri-social-commerce
description: Optimize Cherri's Instagram Shop and TikTok Shop presence. Manage product listings, analyze ad performance, and drive traffic to Shopify. Uses Meta Ads MCP, TikTok Ads MCP, and Chrome MCP for shop management.
---

# Cherri Social Commerce Optimization

Optimize Cherri's presence on Instagram Shop and TikTok Shop:
- **Product optimization**: Titles, descriptions, images (via Shopify sync)
- **Ad performance**: Campaign analytics, audience insights, ROAS tracking
- **Shop management**: Catalog health, listing optimization, promotions
- **Traffic driving**: Strategies to move social shoppers to Shopify

## Prerequisites

| Tool | Status | Required For |
|------|--------|--------------|
| Shopify API | Setup needed | Product optimization (syncs to both platforms) |
| Meta Ads MCP | Ready | Instagram ad analytics, campaign management |
| TikTok Ads MCP | Setup needed | TikTok ad analytics, campaign management |
| Chrome MCP | Ready | Shop management when APIs unavailable |

See `skills/README.md` for setup instructions.

## How Social Commerce Works

```
┌─────────────┐
│   Shopify   │ ← Source of truth for products
│  (optimize  │
│   here)     │
└──────┬──────┘
       │ auto-sync
       ├────────────────┬────────────────┐
       ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Instagram  │  │   TikTok    │  │   Google    │
│    Shop     │  │    Shop     │  │  Shopping   │
└─────────────┘  └─────────────┘  └─────────────┘
       │                │
       ▼                ▼
   Meta Ads          TikTok Ads
   (promote)         (promote)
```

**Key insight:** Optimize products in Shopify → changes flow everywhere.

## Intake Questions

**What social commerce work do you need?**

1. **Product listing audit** - Check catalog health across platforms
2. **Ad performance analysis** - ROAS, CTR, audience insights
3. **Campaign optimization** - Improve underperforming ads
4. **Cross-platform strategy** - Coordinate Instagram + TikTok efforts
5. **Traffic analysis** - Understand social → Shopify conversion

**Provide:**
- Which platform(s) to focus on
- Date range for analysis
- Specific products or campaigns to review
- Goals (awareness, traffic, conversions)

## Workflow: Product Listing Audit

### Step 1: Pull Shopify Product Data

Use Shopify API or Chrome MCP to get:
- All active products
- Titles, descriptions, images
- Variants and pricing
- SEO fields

### Step 2: Check Instagram Shop Sync

Via Chrome MCP → Meta Commerce Manager:
1. Navigate to https://business.facebook.com/commerce
2. Go to Catalog → Items
3. Check for:
   - Sync errors or rejected items
   - Missing images or descriptions
   - Price mismatches
   - Out-of-stock items still showing

**Common issues:**
| Issue | Impact | Fix |
|-------|--------|-----|
| Missing description | Lower discovery | Add in Shopify |
| Low-res images | Poor conversion | Upload 1024x1024+ |
| Price mismatch | Customer confusion | Resync catalog |
| Rejected items | Not visible | Fix policy violations |

### Step 3: Check TikTok Shop Sync

Via Chrome MCP → TikTok Seller Center:
1. Navigate to https://seller.tiktokglobalshop.com
2. Go to Products → Manage Products
3. Check for:
   - Listing quality score
   - Missing required attributes
   - Image compliance issues
   - Category accuracy

### Step 4: Generate Audit Report

```markdown
# Social Commerce Catalog Audit - YYYY-MM-DD

## Summary
- Total Shopify products: X
- Instagram Shop: X synced, X errors
- TikTok Shop: X synced, X errors

## Critical Issues
1. [Issue]: [Products affected] - [Fix]

## Optimization Opportunities
1. [Opportunity]: [Expected impact]

## Action Items
- [ ] Fix sync errors
- [ ] Optimize descriptions for [products]
- [ ] Update images for [products]
```

Save to: `research/social-commerce/catalog-audit-YYYY-MM-DD.md`

## Workflow: Ad Performance Analysis

### Step 1: Pull Meta Ads Data (via MCP)

Using meta-ads MCP:
- Campaign performance (impressions, clicks, spend, ROAS)
- Ad set breakdown (audiences, placements)
- Creative performance (which images/videos work)
- Conversion tracking (add to cart, purchases)

Key metrics:
| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| CTR | >2% | 1-2% | <1% |
| ROAS | >3x | 2-3x | <2x |
| CPM | <$15 | $15-25 | >$25 |
| CPC | <$1 | $1-2 | >$2 |

### Step 2: Pull TikTok Ads Data (via MCP)

Using tiktok-ads MCP:
- Campaign metrics
- Video view rates
- Engagement (likes, comments, shares)
- Conversion events

TikTok-specific metrics:
| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| Video view rate (2s) | >50% | 30-50% | <30% |
| Video completion | >15% | 8-15% | <8% |
| Engagement rate | >5% | 2-5% | <2% |

### Step 3: Cross-Platform Comparison

| Metric | Instagram | TikTok | Winner |
|--------|-----------|--------|--------|
| Spend | $X | $X | - |
| ROAS | Xx | Xx | ? |
| CPA | $X | $X | ? |
| Traffic to Shopify | X | X | ? |

### Step 4: Generate Performance Report

```markdown
# Social Ads Performance Report - [Date Range]

## Executive Summary
- Total spend: $X
- Total revenue attributed: $X
- Blended ROAS: Xx

## Instagram Performance
- Spend: $X | Revenue: $X | ROAS: Xx
- Top performing: [campaign/creative]
- Underperforming: [campaign/creative]

## TikTok Performance
- Spend: $X | Revenue: $X | ROAS: Xx
- Top performing: [campaign/creative]
- Underperforming: [campaign/creative]

## Recommendations
1. [Action]: [Expected impact]
2. [Action]: [Expected impact]
```

Save to: `research/social-commerce/ad-performance-YYYY-MM-DD.md`

## Workflow: Shop Management (Chrome MCP)

### Meta Commerce Manager URLs

| Task | URL |
|------|-----|
| Catalog overview | https://business.facebook.com/commerce/catalogs |
| Product issues | https://business.facebook.com/commerce/catalogs/{id}/diagnostics |
| Shop settings | https://business.facebook.com/commerce/shop |
| Orders | https://business.facebook.com/commerce/orders |
| Insights | https://business.facebook.com/commerce/insights |

### TikTok Seller Center URLs

| Task | URL |
|------|-----|
| Product management | https://seller.tiktokglobalshop.com/product/manage |
| Order management | https://seller.tiktokglobalshop.com/order/list |
| Shop decoration | https://seller.tiktokglobalshop.com/shop/decoration |
| Promotions | https://seller.tiktokglobalshop.com/promotion |
| Analytics | https://seller.tiktokglobalshop.com/compass/dashboard |

## Workflow: Drive Traffic to Shopify

### Strategy 1: Product Page Optimization

Ensure Shopify product pages are optimized for social traffic:
- Fast loading (social users are impatient)
- Mobile-first design
- Clear CTAs
- Social proof (reviews, UGC)
- Easy checkout

### Strategy 2: UTM Tracking

Tag all social links with UTM parameters:
```
?utm_source=instagram&utm_medium=shop&utm_campaign=spring2024
?utm_source=tiktok&utm_medium=shop&utm_campaign=spring2024
```

Check in GA4:
- Session source/medium breakdown
- Conversion rate by source
- Revenue by source

### Strategy 3: Exclusive Offers

Drive social shoppers to Shopify with:
- Social-exclusive discount codes
- Bundle deals only on website
- Free shipping thresholds
- Loyalty program enrollment

### Strategy 4: Content Strategy

| Platform | Content Type | Goal |
|----------|--------------|------|
| Instagram | Lifestyle photos, Stories, Reels | Brand awareness, consideration |
| TikTok | Trending sounds, UGC, tutorials | Discovery, viral reach |
| Both | Product tags, Shop links | Direct conversion |

## Quick Commands

**Catalog health check:**
"Check Instagram and TikTok Shop for sync errors"

**Ad performance:**
"Show me ROAS for Instagram and TikTok ads last 30 days"

**Campaign comparison:**
"Compare performance of Instagram vs TikTok campaigns"

**Traffic analysis:**
"How much traffic are we getting from Instagram Shop to Shopify?"

**Product optimization:**
"Which products need better descriptions for social commerce?"
