---
name: cherri-content-brief
description: Use for generating SEO content briefs for Cherri. Creates detailed briefs for blog posts, collection pages, and product descriptions with keyword targeting, competitor analysis, content outlines, and brand voice guidelines.
---

<purpose>

Generate comprehensive content briefs for Cherri that include:
- **Keyword strategy**: Primary and secondary keywords with intent analysis
- **Competitor content analysis**: What's ranking and why
- **Content outline**: H2/H3 structure with suggested content
- **Brand voice guidelines**: Cherri's tone and messaging
- **Technical specs**: Word count, internal links, CTAs

</purpose>

<cherri_brand_voice>

## Cherri Brand Voice Guidelines

**Tone:** Confident, inclusive, playful yet sophisticated

**Key Messages:**
- Comfort is non-negotiable
- Sustainability matters
- Every body is beautiful
- Quality over quantity

**Words to Use:**
- Comfortable, soft, breathable
- Sustainable, eco-conscious, responsible
- Inclusive, for every body
- Everyday luxury, effortless

**Words to Avoid:**
- Cheap, budget, discount
- Sexy (unless contextually appropriate)
- Perfect (implies imperfection)
- Basic (implies boring)

**Voice Examples:**
- "Feel good in what you wear, every single day."
- "Underwear that works as hard as you do."
- "Soft on your skin. Gentle on the planet."

</cherri_brand_voice>

<intake>

**What type of content brief do you need?**

1. **Blog post brief** - Educational or lifestyle content
2. **Collection page brief** - Category page optimization
3. **Product description brief** - Individual product copy
4. **Landing page brief** - Campaign or seasonal page
5. **FAQ/Help content brief** - Customer support content

**Provide:**
- Target keyword or topic
- Content type (see above)
- Target audience segment (if specific)
- Any competitor content to reference
- Specific products to feature (if applicable)

</intake>

<workflow_blog_brief>

## Blog Post Brief

**Goal:** Create comprehensive brief for SEO-optimized blog content.

### Step 1: Keyword Research

For the target topic, gather:
- Primary keyword (target in title, H1, first 100 words)
- Secondary keywords (3-5, use in H2s and body)
- Related questions (from PAA, use for H2s or FAQ)
- Long-tail variations (weave into content)

**Example for "sustainable underwear":**
```
Primary: sustainable underwear
Secondary: eco-friendly underwear, organic cotton underwear, ethical underwear brands
Questions: Is organic cotton underwear better? How to choose sustainable underwear?
Long-tail: sustainable underwear for women, best sustainable underwear brands 2024
```

### Step 2: Search Intent Analysis

Determine intent:
| Intent | Signals | Content Approach |
|--------|---------|------------------|
| Informational | "what is", "how to", "guide" | Educational, comprehensive |
| Commercial | "best", "review", "vs" | Comparison, recommendations |
| Transactional | "buy", "shop", "price" | Product-focused, CTAs |

### Step 3: Competitor Analysis

For top 3-5 ranking articles:
- Title and H1
- Word count
- H2/H3 structure
- Unique angles
- Gaps/weaknesses

### Step 4: Content Outline

**Brief Template:**

```markdown
# [Blog Post Title - Include Primary Keyword]

**Target Keyword:** [primary keyword]
**Secondary Keywords:** [list]
**Search Intent:** [informational/commercial/transactional]
**Word Count:** [X-Y words]
**Target Audience:** [segment]

## Introduction (100-150 words)
- Hook: [attention-grabbing opening]
- Problem/question addressed
- What reader will learn
- Include primary keyword naturally

## H2: [First Main Section - Include Secondary Keyword]
- Key points to cover
- [Bullet point 1]
- [Bullet point 2]
- Internal link opportunity: [link to relevant product/collection]

## H2: [Second Main Section]
- Key points to cover
- [Supporting data or examples]

## H2: [Third Main Section]
...

## H2: FAQ Section (Optional)
- Q: [Question from PAA]
- Q: [Question from PAA]

## Conclusion (100-150 words)
- Summary of key points
- CTA: [specific action - shop collection, learn more, etc.]

## SEO Checklist
- [ ] Primary keyword in title
- [ ] Primary keyword in first 100 words
- [ ] Primary keyword in at least one H2
- [ ] Secondary keywords distributed in H2s and body
- [ ] Internal links to 2-3 relevant pages
- [ ] External link to 1 authoritative source
- [ ] Meta description written (150-160 chars)
- [ ] Image alt text includes keyword variation
```

### Step 5: Output

Save brief to: `research/content-briefs/blog-[slug]-YYYY-MM-DD.md`

</workflow_blog_brief>

<workflow_collection_brief>

## Collection Page Brief

**Goal:** Optimize category page for search and conversion.

### Step 1: Keyword Mapping

For the collection:
- Primary keyword (category term)
- Secondary keywords (modifiers)
- Product-specific keywords (included products)

**Example for "Cotton Underwear" collection:**
```
Primary: cotton underwear
Secondary: women's cotton underwear, organic cotton underwear, cotton panties
Products: cotton brief, cotton thong, cotton bikini
```

### Step 2: Collection Page Structure

```markdown
# Collection: [Collection Name]

**Target Keyword:** [primary]
**URL:** /collections/[handle]

## SEO Title (50-60 chars)
[Proposed title with keyword]

## Meta Description (150-160 chars)
[Proposed description with keyword and CTA]

## H1
[Collection name - include keyword]

## Collection Description (150-300 words)

### Paragraph 1: Introduction
- What is this collection
- Who it's for
- Include primary keyword

### Paragraph 2: Benefits/Features
- Key selling points
- What makes Cherri different
- Include secondary keyword

### Paragraph 3: Product Variety
- Types of products included
- Sizing information
- Include product keywords

### CTA
- Shop now messaging
- Any current promotions

## Internal Links
- Link to: [related collection]
- Link to: [relevant blog post]

## Schema Markup
- CollectionPage schema
- BreadcrumbList schema
```

### Step 3: Output

Save to: `research/content-briefs/collection-[handle]-YYYY-MM-DD.md`

</workflow_collection_brief>

<workflow_product_brief>

## Product Description Brief

**Goal:** Write compelling, SEO-optimized product copy.

### Step 1: Product Research

Gather:
- Product name and SKU
- Key features (materials, sizing, colors)
- Benefits (comfort, sustainability, etc.)
- Target keywords
- Competitor product descriptions

### Step 2: Product Description Structure

```markdown
# Product: [Product Name]

**SKU:** [SKU]
**Target Keyword:** [primary]
**Collection:** [parent collection]

## SEO Title (50-60 chars)
[Product Name] | [Key Benefit] | Cherri

## Meta Description (150-160 chars)
Shop [product name]. [Key benefit]. [Material/feature]. Available in sizes XS-3XL. Free shipping on $50+.

## Product Title (H1)
[Product Name with keyword]

## Short Description (50-75 words)
[Elevator pitch - what it is, key benefit, who it's for]

## Long Description (150-250 words)

### Opening Hook
[Benefit-focused opening line]

### Features & Benefits
- [Feature 1]: [Benefit 1]
- [Feature 2]: [Benefit 2]
- [Feature 3]: [Benefit 3]

### Materials
[Material details, sustainability angle]

### Sizing & Fit
[Fit description, size range]

### Care
[Care instructions]

## Bullet Points (for product listing)
- [Benefit 1]
- [Benefit 2]
- [Material highlight]
- [Size range]
- [Sustainability angle]

## Image Alt Text
- Main image: [Product name] in [color] - front view
- Image 2: [Product name] - [angle/detail]
```

### Step 3: Output

Save to: `research/content-briefs/product-[handle]-YYYY-MM-DD.md`

</workflow_product_brief>

<content_formulas>

## Content Formulas

### Blog Post Titles
- How to [Achieve Result] with [Product/Method]
- X Best [Products] for [Audience/Use Case]
- [Product] vs [Product]: Which is Right for You?
- The Ultimate Guide to [Topic]
- Why [Benefit] Matters (And How to Get It)

### Product Descriptions
- **Feature + Benefit:** "Made from organic cotton (feature), so it's soft on sensitive skin (benefit)"
- **Problem + Solution:** "Tired of underwear that rides up? Our [product] stays put all day."
- **Social Proof:** "Our bestselling [product] is loved by customers for its [benefit]"

### CTAs
- "Shop [Collection] now"
- "Find your perfect fit"
- "Discover sustainable comfort"
- "Get yours today"

</content_formulas>

<quality_checklist>

## Content Quality Checklist

Before finalizing any brief:

**SEO:**
- [ ] Primary keyword in title, H1, first 100 words
- [ ] Secondary keywords distributed naturally
- [ ] Meta title and description optimized
- [ ] Internal links planned

**Brand:**
- [ ] Tone matches Cherri voice guidelines
- [ ] No forbidden words used
- [ ] Sustainability angle included where relevant
- [ ] Inclusive language throughout

**Structure:**
- [ ] Clear H2/H3 hierarchy
- [ ] Appropriate word count for content type
- [ ] CTA included
- [ ] Scannable format (bullets, short paragraphs)

**User Value:**
- [ ] Answers the search intent
- [ ] Provides unique value vs competitors
- [ ] Actionable takeaways
- [ ] Accurate product/brand information

</quality_checklist>

<quick_commands>

## Quick Commands

**Blog brief:**
"Create a content brief for a blog post about sustainable underwear"

**Collection brief:**
"Write a brief for the Cotton Underwear collection page"

**Product brief:**
"Generate product description brief for the cotton brief"

**Competitor analysis:**
"Analyze top 3 ranking articles for 'best sustainable underwear'"

**Outline only:**
"Just give me an H2 outline for 'how to choose underwear fabric'"

</quick_commands>
