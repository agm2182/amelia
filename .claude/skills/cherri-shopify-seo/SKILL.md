---
name: cherri-shopify-seo
description: Audit Cherri's Shopify storefront SEO. Use for checking meta tags, schema markup, page speed, and technical SEO issues. Generates audit reports and change recommendations. Audits work via Chrome MCP; applying changes requires manual Shopify Admin access.
---

# Cherri Shopify SEO Auditor

Audit Cherri's Shopify store for SEO issues:
- **Meta tag audit**: Check titles, descriptions, OG tags
- **Schema markup**: Validate Product, Organization, BreadcrumbList schemas
- **Page speed**: Audit Core Web Vitals via PageSpeed Insights
- **Technical SEO**: Check canonicals, robots, sitemap, redirects

## Tool Availability

| Capability | Status | Method |
|------------|--------|--------|
| View pages & meta tags | Works | Chrome MCP |
| Check schema markup | Works | Chrome MCP + JSON-LD inspection |
| PageSpeed Insights | Works | Public API (no auth needed) |
| Check robots.txt/sitemap | Works | Direct URL fetch |
| **Apply SEO changes** | Manual | User must edit in Shopify Admin |

**Note:** Shopify Admin API auth is not configured. All change recommendations are generated as CSVs for manual application.

## Intake Questions

**What Shopify SEO work do you need?**

1. **Full technical audit** - Comprehensive SEO health check
2. **Meta tag audit** - Check/optimize titles and descriptions
3. **Schema markup audit** - Validate structured data
4. **Page speed audit** - Core Web Vitals analysis
5. **Generate change recommendations** - Create batch update CSV

**Provide:**
- Specific pages to audit (optional, defaults to key pages)
- Target keywords for optimization (optional)

## Workflow: Full Technical Audit

### Step 1: Crawl Key Pages via Chrome MCP

Navigate to and audit:
- Homepage: https://shopcherri.com
- Top product pages (by traffic from GA4)
- Top collection pages
- Blog landing page
- About/FAQ pages

### Step 2: Meta Tag Check

For each page, verify:

| Element | Check | Good Example |
|---------|-------|--------------|
| Title | 50-60 chars, keyword included, unique | "Women's Cotton Underwear | Cherri" |
| Meta description | 150-160 chars, CTA, keyword | "Shop comfortable cotton underwear..." |
| H1 | One per page, keyword included | "Cotton Underwear for Women" |
| OG title | Same as title or customized | - |
| OG description | Same as meta or customized | - |
| OG image | 1200x630, product/lifestyle image | - |

**How to check via Chrome MCP:**
1. Navigate to page
2. Use `read_page` to get DOM
3. Or use `javascript_tool` to extract:
```javascript
({
  title: document.title,
  metaDesc: document.querySelector('meta[name="description"]')?.content,
  h1: document.querySelector('h1')?.textContent,
  ogTitle: document.querySelector('meta[property="og:title"]')?.content,
  ogDesc: document.querySelector('meta[property="og:description"]')?.content,
  canonical: document.querySelector('link[rel="canonical"]')?.href
})
```

### Step 3: Schema Markup Check

Validate required schemas by extracting JSON-LD:

```javascript
Array.from(document.querySelectorAll('script[type="application/ld+json"]'))
  .map(s => JSON.parse(s.textContent))
```

**Product pages need:**
```json
{
  "@type": "Product",
  "name": "Product name",
  "image": "URL",
  "description": "Description",
  "sku": "SKU",
  "offers": {
    "@type": "Offer",
    "price": "XX.XX",
    "priceCurrency": "USD",
    "availability": "InStock/OutOfStock"
  }
}
```

**Homepage needs:**
```json
{
  "@type": "Organization",
  "name": "Cherri",
  "url": "https://shopcherri.com",
  "logo": "URL",
  "sameAs": ["social URLs"]
}
```

**All pages need:**
```json
{
  "@type": "BreadcrumbList",
  "itemListElement": [...]
}
```

### Step 4: Technical Checks

| Check | Expected | How to Test |
|-------|----------|-------------|
| Canonical tags | Self-referencing, correct | Check `<link rel="canonical">` |
| Robots meta | index,follow (unless intentional) | Check `<meta name="robots">` |
| Sitemap | Present, all pages included | Fetch /sitemap.xml |
| Robots.txt | Not blocking important pages | Fetch /robots.txt |
| HTTPS | All pages secure | No mixed content warnings |

### Step 5: Page Speed Check

Use PageSpeed Insights API (public, no auth):

```
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://shopcherri.com&strategy=mobile
```

Key metrics:

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | <2.5s | 2.5-4s | >4s |
| FID | <100ms | 100-300ms | >300ms |
| CLS | <0.1 | 0.1-0.25 | >0.25 |
| TTFB | <800ms | 800ms-1.8s | >1.8s |

### Step 6: Generate Report

Create audit report with:
- Overall SEO health score
- Critical issues (must fix)
- Warnings (should fix)
- Opportunities (nice to have)
- Page-by-page breakdown

Save to: `research/audits/technical-audit-YYYY-MM-DD.md`

## Workflow: Meta Tag Optimization

### Step 1: Pull Current Meta Tags

For each target page, extract current values via Chrome MCP.

### Step 2: Analyze Issues

Common problems:
- Title too long (truncated in SERP)
- Title too short (missing opportunity)
- Description missing CTA
- Keyword not in title
- Duplicate titles/descriptions

### Step 3: Generate Recommendations

For each page, propose:

```
Page: /products/cotton-brief
Current Title: Cotton Brief - Cherri
Proposed Title: Women's Cotton Brief Underwear | Comfortable & Sustainable | Cherri
Target Keyword: cotton brief underwear

Current Description: [empty]
Proposed Description: Shop our bestselling cotton brief underwear. Soft, breathable, and sustainably made. Available in sizes XS-3XL. Free shipping on orders $50+.
```

### Step 4: Create Change-Set CSV

Generate CSV for manual application:

```csv
page_handle,current_seo_title,proposed_seo_title,current_seo_description,proposed_seo_description,target_keyword
cotton-brief,"Cotton Brief","Women's Cotton Brief | Cherri","","Shop soft cotton briefs...",cotton brief underwear
```

Save to: `research/audits/meta-changes-YYYY-MM-DD.csv`

### Step 5: Apply Changes (Manual)

User applies changes in Shopify Admin:
1. Go to https://admin.shopify.com/store/shop-cherri/products
2. Edit each product
3. Scroll to "Search engine listing"
4. Update title and description
5. Save

## Page Speed Opportunities

Common Shopify issues to flag:

| Issue | Impact | Effort | Priority |
|-------|--------|--------|----------|
| Large images | High | Low | P1 |
| Remove unused apps | High | Low | P1 |
| Lazy load below-fold | Medium | Low | P2 |
| Defer non-critical JS | Medium | Medium | P2 |
| Critical CSS inlining | Medium | High | P3 |

## Quick Commands

**Quick audit:**
"Run a quick SEO check on Cherri's homepage"

**Meta check:**
"Check meta tags for the top 10 product pages"

**Schema validation:**
"Validate Product schema on shopcherri.com/products/cotton-brief"

**Speed check:**
"Run PageSpeed Insights on the homepage"

**Generate change-set:**
"Create meta tag improvements for all collection pages"
