# Cherri Indexing Status Report

Generated: 2026-01-18

## Summary

- **Homepage**: ✅ Indexed (crawled today)
- **Collection pages**: ✅ Indexed
- **Product pages**: ❌ Not indexed (discovered but not crawled)

## Root Cause

Google has discovered product URLs via sitemap and internal links but hasn't prioritized crawling them. This is NOT due to:
- robots.txt blocking (verified - products allowed)
- noindex meta tags (verified - none present)
- Missing canonical tags (verified - correctly set)

The issue is **crawl budget prioritization** - Google sees products as lower priority than collections.

## Indexed Pages

| URL | Status | Last Crawled |
|-----|--------|--------------|
| https://shopcherri.com/ | ✅ Indexed | 2026-01-18 |
| https://shopcherri.com/collections/panties | ✅ Indexed | 2026-01-18 |
| https://shopcherri.com/collections/thong | ✅ Indexed | 2026-01-18 |

## Product Pages Needing Manual Indexing Request

Priority order based on search demand:

### High Priority (Core Products)
1. https://shopcherri.com/products/mid-rise-thong-licorice
2. https://shopcherri.com/products/g-string-licorice
3. https://shopcherri.com/products/high-waist-hipster
4. https://shopcherri.com/products/bikini-brief-guava
5. https://shopcherri.com/products/ruffle-cheeky-taffy

### Medium Priority (Bundles)
6. https://shopcherri.com/products/3-pack-mid-rise-thongs-neapolitan
7. https://shopcherri.com/products/3-pack-bikini-brief-spring-fling
8. https://shopcherri.com/products/3-pack-g-strings-cookie-dough

### Lower Priority (Specialty Items)
9. https://shopcherri.com/products/thong-bodysuit-coconut
10. https://shopcherri.com/products/logo-high-cut-brief-lavender

## Action Items

### Immediate (Manual)
1. Go to [Google Search Console](https://search.google.com/search-console)
2. Use URL Inspection tool for each product URL above
3. Click "Request Indexing" for each

### Technical Improvements
1. Add prominent internal links from homepage to top products
2. Add "Shop Now" CTAs on collection pages linking to individual products
3. Ensure product pages link to related products
4. Consider adding breadcrumb navigation for better crawl paths

## Potential Crawl Signal Issues

GSC shows product URLs being discovered via collection-prefixed paths:
- `/collections/all/products/mid-rise-thong-licorice`
- `/collections/black/products/mid-rise-thong-licorice`

These variant URLs all canonicalize to the correct `/products/` URL, but having multiple discovery paths may dilute crawl signals. The canonical tags ARE correctly set, so this is working as intended.

## Sitemap Status

- Sitemap: https://shopcherri.com/sitemap.xml
- Last submitted: 2026-01-13
- URLs submitted: 122
- URLs indexed: 0 (per GSC report - may be delayed)

Note: The "0 indexed" count appears to be a GSC reporting lag, as URL inspection shows some pages ARE indexed.
