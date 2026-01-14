---
name: cherri-shopify-seo-api
description: Full Shopify SEO management via Admin GraphQL API. Audit AND apply meta tags, schema markup, and SEO fields programmatically. Requires Shopify Admin API access token.
---

# Cherri Shopify SEO (API Version)

Full Shopify SEO management with read/write capabilities:
- **Audit SEO fields**: Pull current meta tags, descriptions across all products/collections
- **Batch updates**: Apply SEO changes via GraphQL mutations
- **Schema validation**: Check and fix structured data
- **Change management**: Generate change-sets, review, then apply

## Prerequisites

This skill requires Shopify Admin API access. See `skills/README.md` for setup instructions.

**Required scopes:**
- `read_products`, `write_products`
- `read_content`, `write_content`
- `read_online_store_pages`, `write_online_store_pages`

## Workflow: Full Technical Audit

### Step 1: Pull All Product SEO Data

```graphql
query getProductsSEO($first: Int!, $after: String) {
  products(first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        handle
        title
        descriptionHtml
        seo {
          title
          description
        }
        featuredImage {
          url
          altText
        }
        onlineStoreUrl
      }
    }
  }
}
```

Paginate through all products (use `first: 50`, follow `endCursor`).

### Step 2: Pull All Collection SEO Data

```graphql
query getCollectionsSEO($first: Int!, $after: String) {
  collections(first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        handle
        title
        descriptionHtml
        seo {
          title
          description
        }
        image {
          url
          altText
        }
      }
    }
  }
}
```

### Step 3: Pull Page SEO Data

```graphql
query getPagesSEO($first: Int!) {
  pages(first: $first) {
    edges {
      node {
        id
        handle
        title
        bodySummary
        seo {
          title
          description
        }
      }
    }
  }
}
```

### Step 4: Analyze SEO Issues

For each item, check:

| Element | Rule | Flag If |
|---------|------|---------|
| SEO Title | 50-60 chars, has keyword | Empty, too long, missing keyword |
| SEO Description | 150-160 chars, has CTA | Empty, too long, no action words |
| Image Alt Text | Descriptive, has keyword | Empty or generic |
| Handle/URL | Lowercase, hyphenated, has keyword | Contains underscores or numbers |

### Step 5: Generate Audit Report

Output CSV with all SEO fields:

```csv
type,id,handle,current_seo_title,title_length,current_seo_description,desc_length,has_image_alt,issues
product,gid://shopify/Product/123,cotton-brief,"Cotton Brief",12,"",0,false,"Missing description, no image alt"
```

Save to: `research/audits/shopify-seo-audit-YYYY-MM-DD.csv`

## Workflow: Batch SEO Updates

### Step 1: Generate Change-Set

Create proposed changes CSV:

```csv
type,id,handle,current_seo_title,proposed_seo_title,current_seo_description,proposed_seo_description,approved
product,gid://shopify/Product/123,cotton-brief,"Cotton Brief","Women's Cotton Brief | Cherri","","Shop soft, sustainable cotton briefs...",
```

Save to: `research/audits/seo-changes-YYYY-MM-DD.csv`

### Step 2: Review Changes

Present changes to user for approval. User marks `approved` column as `true` or `yes`.

### Step 3: Apply Product SEO Updates

For each approved product change:

```graphql
mutation updateProductSEO($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      id
      handle
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

Variables:
```json
{
  "input": {
    "id": "gid://shopify/Product/123",
    "seo": {
      "title": "Women's Cotton Brief | Cherri",
      "description": "Shop soft, sustainable cotton briefs..."
    }
  }
}
```

### Step 4: Apply Collection SEO Updates

```graphql
mutation updateCollectionSEO($input: CollectionInput!) {
  collectionUpdate(input: $input) {
    collection {
      id
      handle
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

### Step 5: Apply Page SEO Updates

```graphql
mutation updatePageSEO($id: ID!, $page: PageUpdateInput!) {
  pageUpdate(id: $id, page: $page) {
    page {
      id
      handle
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

### Step 6: Verify Changes

Re-query updated items to confirm changes applied. Generate verification report.

Save to: `research/audits/seo-changes-applied-YYYY-MM-DD.csv`

## Workflow: Image Alt Text Updates

### Step 1: Find Missing Alt Text

```graphql
query getProductImages($first: Int!) {
  products(first: $first) {
    edges {
      node {
        id
        handle
        title
        images(first: 10) {
          edges {
            node {
              id
              url
              altText
            }
          }
        }
      }
    }
  }
}
```

Filter for images where `altText` is null or empty.

### Step 2: Generate Alt Text Recommendations

For each image, propose alt text based on:
- Product title
- Image position (main, lifestyle, detail)
- Color/variant if visible

Format: `[Product Name] in [Color] - [View Type]`

Example: "Cotton Brief in Blush - Front View"

### Step 3: Apply Alt Text Updates

```graphql
mutation updateProductImage($productId: ID!, $image: ImageInput!) {
  productImageUpdate(productId: $productId, image: $image) {
    image {
      id
      altText
    }
    userErrors {
      field
      message
    }
  }
}
```

## Workflow: URL/Handle Optimization

### Step 1: Audit Handles

Check all product/collection handles for:
- Underscores (should be hyphens)
- Random numbers
- Missing keywords
- Too long (>60 chars)

### Step 2: Generate Redirect Plan

**WARNING:** Changing handles breaks existing URLs. Must create redirects.

```csv
type,old_handle,new_handle,old_url,new_url,redirect_needed
product,cotton_brief_01,cotton-brief,/products/cotton_brief_01,/products/cotton-brief,true
```

### Step 3: Apply Handle Change + Redirect

```graphql
mutation updateProductHandle($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      id
      handle
    }
    userErrors {
      field
      message
    }
  }
}
```

Then create redirect:

```graphql
mutation createRedirect($urlRedirect: UrlRedirectInput!) {
  urlRedirectCreate(urlRedirect: $urlRedirect) {
    urlRedirect {
      id
      path
      target
    }
    userErrors {
      field
      message
    }
  }
}
```

## Rate Limits

Shopify GraphQL Admin API has rate limits based on calculated query cost.

**Best practices:**
- Batch queries where possible
- Use pagination (50 items per request)
- Add delays between mutations (100ms)
- Monitor `X-Shopify-Shop-Api-Call-Limit` header

## Quick Commands

**Full audit:**
"Pull all product and collection SEO data and generate audit report"

**Update product SEO:**
"Update SEO title and description for the cotton-brief product"

**Batch update:**
"Apply all approved changes from the change-set CSV"

**Fix alt text:**
"Find all products with missing image alt text and generate recommendations"

**Check handles:**
"Audit all product handles for SEO issues"
