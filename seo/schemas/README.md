# SEO Schema Markup

JSON-LD structured data schemas ready to be added to Shopify pages.

## How to Apply

### Option 1: Theme App Extension (Recommended)
Add schemas via a Shopify app like JSON-LD for SEO or Schema Plus.

### Option 2: Theme Code
Add to the relevant template in `theme.liquid` or page-specific templates:

```liquid
{% if template contains 'collection' and collection.handle == 'wide-gusset' %}
<script type="application/ld+json">
  {%- render 'schema-wide-gusset-faq' -%}
</script>
{% endif %}
```

### Option 3: Shopify Metafields
Store schema JSON in a metafield and render in theme.

## Available Schemas

| File | Page | Schema Type |
|------|------|-------------|
| `wide-gusset-faq.json` | /collections/wide-gusset | FAQPage |

## Validation

Test schemas before deploying:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)
