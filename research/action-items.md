# Cherri SEO Action Items

Running list of fixes and improvements identified during research.

---

## Quick Fixes (Do This Week)

### Analytics & Tracking
- [ ] **Enable Shopify bot filtering** - Add "Human or bot session" filter to Shopify Analytics reports to get clean conversion data
  - Go to: Admin → Analytics → Add dimension → "Human or bot session"
  - Filter to "Human" for accurate metrics
  - Note: Only works for data from Oct 7, 2025 onward

- [ ] **Create GA4 bot exclusion segment** - Filter out high-bounce product pages from GA4 reports
  - Exclude sessions landing on pages with 98%+ bounce rate
  - Or create segment: Device = Mobile only (desktop is 96.5% bots)

### Product Schema (Critical for Rich Snippets)
- [ ] **Fix brand field** - Currently malformed, needs to be Organization object
- [ ] **Add priceValidUntil** - Missing on all product variants
- [ ] **Add shippingDetails** - Required for Merchant Listings
- [ ] **Add hasMerchantReturnPolicy** - Required for Merchant Listings
- [ ] **Integrate reviews app** - Needed for `review` and `aggregateRating` fields

---

## High Priority (This Month)

### SEO Optimization
- [ ] **Wait for GSC data** - Re-check search analytics Jan 15-16 for keyword data
- [ ] **Optimize /collections/panties** - Add SEO title and description targeting "women's underwear" keywords
- [ ] **Optimize /collections/thong** - High engagement (83%), good SEO target
- [ ] **Optimize /collections/swimwear** - Getting organic traffic but 0 conversions

### Content
- [ ] **Create first blog post** - Use cherri-content-brief skill
- [ ] **Expand "underwear pocket" article** - Already ranking, has 45% bounce (good engagement)

---

## Medium Priority (This Quarter)

### Content Strategy
- [ ] **Build content calendar** - Target 1-2 posts per week
- [ ] **Topic ideas:**
  - Underwear fabric guide (cotton vs modal vs bamboo)
  - Sizing guide for different body types
  - Sustainability in underwear manufacturing
  - How to care for delicate underwear
  - Best underwear for working out
  - What to look for in comfortable underwear

### Technical SEO
- [ ] **Add breadcrumbs** - Check if theme has them, enable if not
- [ ] **Internal linking audit** - Link blog posts to collections
- [ ] **Image alt text audit** - Ensure product images have keyword-rich alt text

---

## Completed

- [x] Submit sitemap to GSC (Jan 13, 2026)
- [x] Verify site indexing status (Jan 13, 2026)
- [x] Complete initial SEO audit (Jan 13, 2026)
- [x] Set up GSC MCP connection
- [x] Set up GA4 MCP connection

---

## Notes

**Bot Traffic Pattern Identified:**
- Specific product pages getting 5,000+ sessions with 98%+ bounce
- Classified as "Direct" traffic
- Likely TikTok in-app browser (doesn't pass referrer)
- Desktop traffic is 96.5% bounce vs Mobile 45.9%

**Key Metrics to Improve:**
| Metric | Current | Target (90 days) |
|--------|---------|------------------|
| Organic Sessions | 3,756/mo | 7,500/mo |
| Organic Revenue | $3,970/mo | $8,000/mo |
| Blog Posts | 3 | 15+ |

---

*Last updated: January 13, 2026*
