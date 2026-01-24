# SEO Schema Markup for AEO (Answer Engine Optimization)

JSON-LD structured data schemas ready to be added to Shopify pages for improved visibility in AI-powered search engines (Google AI Overviews, ChatGPT, Perplexity, etc.).

## Available Schemas

| File | Target Page | Schema Type | Priority |
|------|-------------|-------------|----------|
| `faq-page.json` | /pages/contact | FAQPage | P0 - Deploy now |
| `wide-gusset-faq.json` | /collections/wide-gusset | FAQPage | P0 - Deploy now |
| `organization.json` | Site-wide | Organization | P0 - Fixes null sameAs |
| `breadcrumb-collection.liquid` | Collection pages | BreadcrumbList | P1 |
| `breadcrumb-product.liquid` | Product pages | BreadcrumbList | P1 |
| `product-enhanced.liquid` | Product pages | Product | P1 - Fixes audit issues |

## Current Issues (From Audit)

The live site has these schema problems:

1. **Organization schema** - `sameAs` array contains 7 null values
2. **Product schema**:
   - `brand` field uses `@type: "Thing"` instead of `@type: "Organization"`
   - Missing `priceValidUntil` on all offers
   - Missing `shippingDetails`
   - Missing `hasMerchantReturnPolicy`
   - Missing `material` field
3. **No BreadcrumbList schema** on any pages
4. **No FAQPage schema** despite having FAQ content

## Deployment Options

### Option 1: Theme Code (Recommended for Liquid templates)

Edit the theme in Shopify Admin > Online Store > Themes > Edit code:

**For Organization schema fix:**
1. Find `snippets/` or where the current Organization schema is defined
2. Replace the schema with contents of `organization.json`
3. Or update Social Media settings in Theme > Customize > Footer to remove empty links

**For Breadcrumb schemas:**
1. Create new snippets: `schema-breadcrumb-collection.liquid` and `schema-breadcrumb-product.liquid`
2. Copy contents from the `.liquid` files in this folder
3. Include in templates:
   - `sections/main-collection.liquid`: `{% render 'schema-breadcrumb-collection' %}`
   - `sections/main-product.liquid`: `{% render 'schema-breadcrumb-product' %}`

**For Product schema:**
1. Find existing product schema (usually in `snippets/` or `sections/main-product.liquid`)
2. Replace with contents of `product-enhanced.liquid`

### Option 2: Metafields (For JSON schemas on specific pages)

Add FAQ schemas to specific pages via Shopify Admin API:

```bash
# Get the page ID first
ACCESS_TOKEN=$(cat ~/.config/cherri/shopify-credentials.json | jq -r .access_token)

# Create metafield for FAQ page (ID: 26078249019)
curl -X POST "https://shop-cherri.myshopify.com/admin/api/2025-01/pages/26078249019/metafields.json" \
  -H "X-Shopify-Access-Token: $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "metafield": {
      "namespace": "seo",
      "key": "json_ld",
      "value": "<contents of faq-page.json>",
      "type": "json"
    }
  }'
```

Then render in theme:
```liquid
{% if page.metafields.seo.json_ld %}
<script type="application/ld+json">
{{ page.metafields.seo.json_ld }}
</script>
{% endif %}
```

### Option 3: Third-Party App

Apps like JSON-LD for SEO, Schema Plus, or Smart SEO can manage schema automatically:
- Automatically generate product, collection, and breadcrumb schemas
- FAQ schema still needs manual addition via metafields
- May have monthly cost

## Quick Deploy: FAQ Schemas via Shopify Admin

### FAQ Page Schema

1. Go to Shopify Admin > Settings > Custom data > Pages
2. Add metafield definition:
   - Name: `SEO JSON-LD`
   - Namespace: `seo`
   - Key: `json_ld`
   - Type: JSON
3. Go to Products > Pages > FAQ's
4. Scroll to metafields section
5. Paste contents of `faq-page.json`
6. Save

### Wide Gusset Collection FAQ Schema

1. Go to Shopify Admin > Settings > Custom data > Collections
2. Add same metafield definition as above
3. Go to Products > Collections > Wide Gusset
4. Paste contents of `wide-gusset-faq.json`
5. Save

### Theme Code for Metafield Rendering

Add to `layout/theme.liquid` before `</head>`:

```liquid
{%- if template contains 'page' and page.metafields.seo.json_ld -%}
<script type="application/ld+json">
{{ page.metafields.seo.json_ld }}
</script>
{%- endif -%}

{%- if template contains 'collection' and collection.metafields.seo.json_ld -%}
<script type="application/ld+json">
{{ collection.metafields.seo.json_ld }}
</script>
{%- endif -%}
```

## Validation

Test all schemas before deploying:

1. **Google Rich Results Test**: https://search.google.com/test/rich-results
2. **Schema.org Validator**: https://validator.schema.org/
3. **Google Search Console**: Monitor Rich Results report after deployment

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| FAQ rich results eligible | 0 pages | 2+ pages |
| Schema validation errors | Multiple | 0 |
| Organization sameAs nulls | 7 | 0 |
| BreadcrumbList coverage | 0% | 100% (collections + products) |
| Product schema complete | No | Yes |

## Files Reference

```
seo/schemas/
├── README.md                      # This file
├── faq-page.json                  # FAQ schema for /pages/contact
├── wide-gusset-faq.json           # FAQ schema for /collections/wide-gusset
├── organization.json              # Fixed Organization schema
├── breadcrumb-collection.liquid   # BreadcrumbList for collections
├── breadcrumb-product.liquid      # BreadcrumbList for products
└── product-enhanced.liquid        # Enhanced Product schema
```
