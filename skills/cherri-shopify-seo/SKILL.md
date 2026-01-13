---
name: cherri-shopify-seo
description: Use for auditing and optimizing Cherri's Shopify storefront SEO. Checks meta tags, schema markup, page speed, and generates improvement change-sets for review before applying via Shopify Admin GraphQL.
---

<purpose>

Audit and optimize Cherri's Shopify store for SEO:
- **Meta tag audit**: Check titles, descriptions, OG tags
- **Schema markup**: Validate Product, Organization, BreadcrumbList schemas
- **Page speed**: Audit Core Web Vitals via PageSpeed Insights
- **Technical SEO**: Check canonicals, robots, sitemap, redirects
- **Change management**: Generate safe change-sets for review before applying

</purpose>

<intake>

**What Shopify SEO work do you need?**

1. **Full technical audit** - Comprehensive SEO health check
2. **Meta tag audit** - Check/optimize titles and descriptions
3. **Schema markup audit** - Validate structured data
4. **Page speed audit** - Core Web Vitals analysis
5. **Product page optimization** - Optimize specific product SEO
6. **Collection page optimization** - Optimize category pages
7. **Generate change-set** - Create batch updates for review

**Provide:**
- Cherri's Shopify store URL
- Specific pages to audit (optional)
- Target keywords for optimization (optional)
- Access to Shopify Admin (for applying changes)

</intake>

<workflow_full_audit>

## Full Technical SEO Audit

**Goal:** Comprehensive health check of Cherri's Shopify SEO.

### Step 1: Crawl Key Pages

Sample pages to audit:
- Homepage
- Top 10 product pages (by traffic)
- Top 5 collection pages
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

### Step 3: Schema Markup Check

Validate required schemas:

**Product pages:**
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

**Organization (homepage):**
```json
{
  "@type": "Organization",
  "name": "Cherri",
  "url": "https://...",
  "logo": "URL",
  "sameAs": ["social URLs"]
}
```

**BreadcrumbList (all pages):**
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
| Sitemap | Present, all pages included | Check /sitemap.xml |
| Robots.txt | Not blocking important pages | Check /robots.txt |
| HTTPS | All pages secure | No mixed content |
| Mobile friendly | Passes Google test | Mobile-Friendly Test |

### Step 5: Page Speed Check

Run PageSpeed Insights for key pages:
- Mobile score (target: >50, ideal: >70)
- Desktop score (target: >70, ideal: >90)
- Core Web Vitals:
  - LCP (target: <2.5s)
  - FID (target: <100ms)
  - CLS (target: <0.1)

### Step 6: Generate Report

Audit report with:
- Overall SEO health score
- Critical issues (must fix)
- Warnings (should fix)
- Opportunities (nice to have)
- Page-by-page breakdown

Save to: `research/audits/technical-audit-YYYY-MM-DD.md`

</workflow_full_audit>

<workflow_meta_optimization>

## Meta Tag Optimization

**Goal:** Optimize titles and descriptions for target pages.

### Step 1: Pull Current Meta Tags

For each page:
- Current title
- Current description
- Target keyword
- Current ranking (from GSC)

### Step 2: Analyze Issues

Common problems:
- Title too long (truncated in SERP)
- Title too short (missing opportunity)
- Description missing CTA
- Keyword not in title
- Duplicate titles/descriptions

### Step 3: Generate Optimized Tags

For each page, propose:

```
Page: /products/cotton-brief
Current Title: Cotton Brief - Cherri
Proposed Title: Women's Cotton Brief Underwear | Comfortable & Sustainable | Cherri
Target Keyword: cotton brief underwear

Current Description: [empty]
Proposed Description: Shop our bestselling cotton brief underwear. Soft, breathable, and sustainably made. Available in sizes XS-3XL. Free shipping on orders $50+.
```

### Step 4: Create Change-Set

Generate CSV for review:
```csv
page_handle,current_title,proposed_title,current_description,proposed_description,target_keyword
```

Save to: `research/audits/meta-changes-YYYY-MM-DD.csv`

### Step 5: Apply Changes (After Review)

Use Shopify Admin GraphQL to apply:
```graphql
mutation updateProductMetafields($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      id
      seo {
        title
        description
      }
    }
  }
}
```

</workflow_meta_optimization>

<workflow_page_speed>

## Page Speed Audit

**Goal:** Identify and fix Core Web Vitals issues.

### Step 1: Run PageSpeed Insights

API endpoint:
```
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={URL}&strategy={mobile|desktop}
```

Test pages:
- Homepage
- Top 3 product pages
- Top 2 collection pages

### Step 2: Analyze Results

Key metrics:
| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | <2.5s | 2.5-4s | >4s |
| FID | <100ms | 100-300ms | >300ms |
| CLS | <0.1 | 0.1-0.25 | >0.25 |
| TTFB | <800ms | 800ms-1.8s | >1.8s |

### Step 3: Identify Opportunities

Common Shopify issues:
- **Large images**: Need WebP/AVIF conversion, lazy loading
- **Render-blocking JS**: Third-party apps, tracking scripts
- **Unused CSS**: Theme bloat
- **Font loading**: Missing font-display: swap
- **App script overhead**: Review installed apps

### Step 4: Prioritize Fixes

| Issue | Impact | Effort | Priority |
|-------|--------|--------|----------|
| Image optimization | High | Low | P1 |
| Remove unused apps | High | Low | P1 |
| Lazy load below-fold | Medium | Low | P2 |
| Defer non-critical JS | Medium | Medium | P2 |
| Critical CSS inlining | Medium | High | P3 |

### Step 5: Output

Speed audit report:
- Current scores (mobile/desktop)
- Core Web Vitals status
- Prioritized fix list
- Expected improvement estimates

Save to: `research/audits/page-speed-YYYY-MM-DD.md`

</workflow_page_speed>

<shopify_graphql_reference>

## Shopify Admin GraphQL Reference

**Use Shopify Dev MCP to explore schemas and validate queries.**

### Common SEO Operations

**Get product SEO fields:**
```graphql
query getProductSEO($id: ID!) {
  product(id: $id) {
    id
    handle
    title
    seo {
      title
      description
    }
    metafields(first: 10) {
      edges {
        node {
          namespace
          key
          value
        }
      }
    }
  }
}
```

**Update product SEO:**
```graphql
mutation updateProductSEO($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
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

**Get collection SEO:**
```graphql
query getCollectionSEO($id: ID!) {
  collection(id: $id) {
    id
    handle
    title
    seo {
      title
      description
    }
  }
}
```

### Safe Change Process

1. **Generate change-set** (CSV with current/proposed values)
2. **Human review** (approve changes before applying)
3. **Dry run** (query current values to confirm IDs)
4. **Apply in batches** (10-20 items at a time)
5. **Verify** (re-query to confirm changes applied)

</shopify_graphql_reference>

<change_set_format>

## Change-Set Format

All proposed changes must be generated as reviewable change-sets before applying.

**Product SEO Changes:**
```csv
product_id,handle,current_seo_title,proposed_seo_title,current_seo_description,proposed_seo_description,approved
gid://shopify/Product/123,cotton-brief,"Cotton Brief","Women's Cotton Brief | Cherri","","Shop soft cotton briefs...",
```

**Collection SEO Changes:**
```csv
collection_id,handle,current_seo_title,proposed_seo_title,current_seo_description,proposed_seo_description,approved
gid://shopify/Collection/456,underwear,"Underwear","Women's Underwear Collection | Cherri","","Shop our full underwear collection...",
```

**Applying Changes:**
Only apply rows where `approved` column = `true` or `yes`.

</change_set_format>

<quick_commands>

## Quick Commands

**Quick audit:**
"Run a quick SEO check on Cherri's homepage"

**Meta check:**
"Check meta tags for the top 10 product pages"

**Schema validation:**
"Validate Product schema on /products/cotton-brief"

**Speed check:**
"Run PageSpeed Insights on the homepage"

**Generate change-set:**
"Create meta tag improvements for all collection pages"

</quick_commands>
