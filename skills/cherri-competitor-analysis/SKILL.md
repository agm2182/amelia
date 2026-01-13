---
name: cherri-competitor-analysis
description: Use for competitive intelligence on Cherri's underwear/intimates competitors. Monitors rankings, identifies content gaps, tracks backlink profiles via Ahrefs, and generates competitive intelligence reports.
---

<purpose>

Track and analyze Cherri's competitors in the underwear/intimates space:
- **Ranking monitoring**: Track competitor positions for target keywords
- **Content analysis**: Identify what content competitors are publishing
- **Backlink intelligence**: Understand competitor link building (via Ahrefs)
- **SERP feature tracking**: Monitor featured snippets, PAA, etc.

</purpose>

<competitor_profiles>

## Primary Competitors

| Competitor | Domain | Positioning | Key Differentiator |
|------------|--------|-------------|-------------------|
| Parade | parade.com | Sustainable, colorful | Bold colors, recycled materials |
| Tommy John | tommyjohn.com | Premium comfort | "No adjustment" technology |
| MeUndies | meundies.com | Fun, subscription | Matching prints, monthly subscription |
| Cuup | cuup.com | Inclusive sizing | Extended size range, fit focus |
| ThirdLove | thirdlove.com | Perfect fit | Half-sizes, fit quiz |

Add/modify competitors as needed for specific analyses.

</competitor_profiles>

<intake>

**What competitive analysis do you need?**

1. **Ranking comparison** - Compare Cherri vs competitors for target keywords
2. **Content gap analysis** - Find content competitors have that Cherri doesn't
3. **Backlink analysis** - Analyze competitor link profiles and opportunities
4. **SERP feature audit** - See which competitors own featured snippets, PAA
5. **New content monitoring** - Track what competitors published recently
6. **Full competitive report** - Comprehensive analysis across all dimensions

**Provide:**
- Specific competitors to analyze (or use defaults)
- Target keyword set (or use Cherri's priority keywords)
- Time period for analysis
- Specific product categories to focus on (optional)

</intake>

<workflow_ranking_comparison>

## Ranking Comparison

**Goal:** See how Cherri stacks up against competitors for target keywords.

### Step 1: Define Keyword Set

Use priority keywords for Cherri:
- Category terms: "underwear", "panties", "bras"
- Branded modifiers: "sustainable underwear", "organic cotton underwear"
- Product-specific: "[product name] review", "best [category]"

### Step 2: Pull Rankings

From Semrush, for each keyword:
- Get Cherri's position
- Get each competitor's position
- Note any SERP features present

### Step 3: Create Comparison Matrix

| Keyword | Cherri | Parade | Tommy John | MeUndies | Leader |
|---------|--------|--------|------------|----------|--------|
| sustainable underwear | 12 | 3 | - | 8 | Parade |
| comfortable panties | 5 | 7 | 2 | 15 | Tommy John |

### Step 4: Identify Patterns

Analyze:
- Keywords where Cherri leads
- Keywords where Cherri trails badly (>10 position gap)
- Keywords no one owns (opportunity)
- Competitors with most #1 positions

### Step 5: Output

Generate comparison report with:
- Visibility score per competitor (sum of 1/position for all keywords)
- Win/loss summary
- Biggest gaps to close
- Quick wins (where Cherri is close to leading)

Save to: `research/competitors/ranking-comparison-YYYY-MM-DD.csv`

</workflow_ranking_comparison>

<workflow_content_gap>

## Content Gap Analysis

**Goal:** Find content competitors have that Cherri doesn't.

### Step 1: Inventory Competitor Content

For each competitor, identify:
- Blog posts and guides
- Product category pages
- Educational content
- Comparison pages
- Resource pages

### Step 2: Map to Keywords

Match each piece of competitor content to:
- Primary keyword target
- Rankings achieved
- Traffic estimate (from Semrush)

### Step 3: Compare to Cherri

Cross-reference with Cherri's content:
- Content Cherri has
- Content Cherri lacks
- Content where Cherri's version underperforms

### Step 4: Prioritize Gaps

Score gaps by:
```
Gap Priority = (Competitor Traffic) × (Keyword Relevance) × (Production Difficulty Inverse)
```

### Step 5: Output

Generate content gap report:
- Gap topic/keyword
- Which competitors have content
- Their estimated traffic
- Recommended content type for Cherri
- Priority score

Save to: `research/competitors/content-gap-YYYY-MM-DD.csv`

</workflow_content_gap>

<workflow_backlink_analysis>

## Backlink Analysis (Ahrefs)

**Goal:** Understand competitor link profiles and find link opportunities.

### Step 1: Pull Competitor Link Data

From Ahrefs API, for each competitor:
- Domain Rating (DR)
- Total backlinks
- Referring domains
- New links (last 30 days)
- Lost links (last 30 days)

### Step 2: Compare Link Metrics

| Metric | Cherri | Parade | Tommy John | MeUndies |
|--------|--------|--------|------------|----------|
| Domain Rating | ? | 65 | 72 | 58 |
| Referring Domains | ? | 2,400 | 3,100 | 1,800 |
| New Links (30d) | ? | 150 | 200 | 90 |

### Step 3: Identify Link Opportunities

Find pages linking to competitors but not Cherri:
- "Best sustainable underwear" roundups
- Fashion/lifestyle publications
- Sustainability blogs
- Gift guides

### Step 4: Analyze Top Links

For each competitor's top 20 backlinks:
- Source domain
- DR of linking domain
- Anchor text
- Page linked to
- Link type (follow/nofollow)

### Step 5: Output

Generate backlink intelligence report:
- Link profile comparison summary
- Top 50 link opportunities (sites linking to competitors but not Cherri)
- Anchor text distribution analysis
- Link velocity comparison

Save to: `research/competitors/backlink-analysis-YYYY-MM-DD.csv`

**Note:** Ahrefs API required. Store key in `.env` as `AHREFS_API_KEY`.

</workflow_backlink_analysis>

<workflow_serp_features>

## SERP Feature Audit

**Goal:** Track which competitors own valuable SERP features.

### Step 1: Define Priority SERPs

Target SERPs with valuable features:
- Featured snippets
- People Also Ask (PAA)
- Product carousels
- Image packs
- Video results

### Step 2: Audit Each SERP

For each priority keyword:
- Which SERP features present?
- Who owns each feature?
- What content earns the feature?

### Step 3: Map Opportunities

Identify:
- Features Cherri could win
- Content format required (list, table, FAQ)
- Current feature holders to outrank

### Step 4: Output

Generate SERP feature report:
- Keyword
- Feature type
- Current owner
- Owner's content format
- Cherri's opportunity
- Required content changes

Save to: `research/competitors/serp-features-YYYY-MM-DD.csv`

</workflow_serp_features>

<workflow_full_report>

## Full Competitive Intelligence Report

**Goal:** Comprehensive quarterly competitor analysis.

### Components

1. **Executive Summary**
   - Market positioning map
   - Key findings (3-5 bullets)
   - Priority actions

2. **Ranking Analysis**
   - Visibility trends (3-month)
   - Keyword wins/losses
   - Share of voice by category

3. **Content Analysis**
   - Content gap summary
   - Competitor content velocity
   - Top performing competitor content

4. **Backlink Analysis**
   - Link profile comparison
   - Link velocity trends
   - Top link opportunities

5. **SERP Features**
   - Feature ownership map
   - Opportunity prioritization

6. **Recommendations**
   - Quick wins (0-30 days)
   - Medium-term plays (30-90 days)
   - Strategic initiatives (90+ days)

### Output

Full report saved to: `research/competitors/competitive-report-YYYY-Q#.md`
Supporting data: `research/competitors/competitive-report-YYYY-Q#-data/`

</workflow_full_report>

<ahrefs_api_reference>

## Ahrefs API Usage

**Base URL:** `https://api.ahrefs.com/v3/`

**Key Endpoints:**

| Endpoint | Purpose |
|----------|---------|
| `/site-explorer/overview` | Domain metrics |
| `/site-explorer/backlinks` | Backlink list |
| `/site-explorer/refdomains` | Referring domains |
| `/keywords-explorer/keywords-by-search` | Keyword data |

**Authentication:**
```bash
curl -H "Authorization: Bearer $AHREFS_API_KEY" \
  "https://api.ahrefs.com/v3/site-explorer/overview?target=competitor.com"
```

**Rate Limits:** Check your subscription tier

</ahrefs_api_reference>

<quick_commands>

## Quick Commands

**Quick ranking check:**
"How does Cherri rank vs Parade for 'sustainable underwear'?"

**Content gap scan:**
"What blog content does MeUndies have that Cherri doesn't?"

**Link opportunity:**
"Find sites linking to Tommy John but not Cherri"

**SERP check:**
"Who owns the featured snippet for 'best cotton underwear'?"

</quick_commands>
