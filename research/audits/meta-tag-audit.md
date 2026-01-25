# Cherri Meta Tag Audit Report

Generated: 2026-01-18

## Executive Summary

**Critical Issues Found:**
1. Homepage title is only 6 characters ("Cherri") - should be ~50-60 chars
2. Collection pages use duplicate meta descriptions
3. Collection page titles are generic (e.g., "Swimwear – Cherri")
4. Product pages are properly optimized ✅

## Current State

### Homepage
| Element | Current | Issue | Recommended |
|---------|---------|-------|-------------|
| Title | "Cherri" (6 chars) | Too short, no keywords | "Cherri - Wide Gusset Organic Underwear | Size XS-4X" (53 chars) |
| Description | Generic 104 chars | Same as all collection pages | Unique, compelling description with CTA |

### Collection Pages (All Using Same Description)

| Page | Title | CTR | Position | Issue |
|------|-------|-----|----------|-------|
| /collections/all | "All Products – Cherri" | 0% | 2.3 | Generic, 0 clicks despite #2 position |
| /collections/swimwear | "Swimwear – Cherri" | 2.3% | 4.4 | Generic title |
| /collections/thong | "Women's Thongs..." ✅ | 2.2% | 2.8 | Has custom title, still low CTR |
| /collections/panties | "Women's Panties..." ✅ | 1.7% | 11.7 | Has custom title, needs CTR boost |
| /collections/bras | Unknown | 1.1% | 7.2 | Needs audit |

**Duplicate Description Used (104 chars):**
> "Organic, lip slip free, wide gusset, vulva positive, ethically produced undies, intimates, and swimwear."

This generic description appears on:
- Homepage
- /collections/all
- /collections/swimwear
- Multiple other collection pages

### Product Pages (Good ✅)

| Page | Title | Description |
|------|-------|-------------|
| /products/bikini-brief-guava | "Bikini Brief - Wide Gusset Underwear \| Cherri" (45 chars) | Custom, product-specific (138 chars) |
| /products/mid-rise-thong-licorice | "Mid-Rise Thong - Wide Gusset Comfort \| Cherri" (46 chars) | Custom (138 chars) |

Product pages have proper unique meta tags.

## Impact Analysis

### Lost Click Opportunities

| Page | Impressions | Current CTR | Target CTR | Potential Additional Clicks |
|------|-------------|-------------|------------|----------------------------|
| /collections/all | 1,176 | 0% | 3% | +35 clicks |
| /collections/panties | 2,201 | 1.7% | 4% | +50 clicks |
| /collections/swimwear | 1,327 | 2.3% | 5% | +35 clicks |
| /collections/thong | 1,289 | 2.2% | 5% | +36 clicks |
| Homepage | 2,445 | 13.7% | 18% | +105 clicks |

**Estimated total opportunity: +260 additional clicks/quarter**

## Recommended Meta Tags

### Homepage
```
Title: Cherri - Wide Gusset Organic Underwear | Sizes XS-4X
Description: Shop Cherri's signature wide gusset underwear in organic Supima cotton. Thongs, briefs & bikinis designed for all-day comfort. Free shipping over $80.
```

### /collections/all → Consider redirecting to /collections/panties or hiding from search
```
Title: Shop All Cherri Underwear & Swimwear | Wide Gusset Comfort
Description: Browse Cherri's complete collection of organic cotton underwear and swimwear. Wide gusset design for all-day comfort in sizes XS-4X. Free shipping $80+.
```

### /collections/swimwear
```
Title: Women's Swimwear - Wide Gusset Bikinis & One-Pieces | Cherri
Description: Shop Cherri swimwear with our signature wide gusset liner. Comfortable bikini bottoms & one-pieces in organic fabrics. Sizes XS-4X, free shipping over $80.
```

### /collections/thong
```
Title: Women's Thongs - Wide Gusset Comfort | Organic Cotton | Cherri
Description: Shop Cherri thongs with extra-wide gussets for all-day comfort. G-strings, mid-rise & high-rise styles in organic Supima cotton. Sizes XS-4X.
```

### /collections/panties (Already has decent title)
Current title is good. Update description:
```
Description: Discover Cherri's wide gusset panties for unmatched comfort. Organic cotton thongs, bikinis, briefs & hipsters. Size-inclusive XS-4X. Free shipping $80+.
```

### /collections/bras
```
Title: Women's Bras & Bralettes - Organic Cotton | Cherri
Description: Shop comfortable bralettes and bodysuits from Cherri. Made with organic cotton for all-day softness. Sizes XS-4X, free shipping over $80.
```

## Implementation Guide (Shopify)

### Option 1: Via Shopify Admin (Easiest)

1. Go to **Online Store > Preferences** for homepage SEO
2. Go to **Products > Collections > [Collection Name]** > scroll to "Search engine listing"
3. Click "Edit" to customize title and description

### Option 2: Via Shopify API (Recommended for Bulk Updates)

Use the Shopify Admin API to update collection metafields:

```graphql
mutation updateCollection($input: CollectionInput!) {
  collectionUpdate(input: $input) {
    collection {
      id
      seo {
        title
        description
      }
    }
    userErrors {
      field
      message
    }
  }
}
```

### Option 3: Via Theme Liquid (For Dynamic Titles)

Edit `theme.liquid` or `collection.liquid` to generate dynamic titles based on collection content.

## Priority Order

1. **CRITICAL**: Fix homepage title (highest impression page)
2. **HIGH**: Fix /collections/all (0% CTR disaster)
3. **HIGH**: Fix /collections/swimwear, /collections/thong (high impressions)
4. **MEDIUM**: Add unique descriptions to all collections
5. **LOW**: Monitor and iterate based on CTR changes

## Verification Steps

After implementation:
1. Use GSC URL Inspection to request re-indexing of updated pages
2. Wait 1-2 weeks for Google to recrawl
3. Compare CTR before/after in GSC
4. Target: 50% improvement in CTR for optimized pages
