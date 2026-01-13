---
name: cherri-keyword-research
description: Use for keyword research and opportunity discovery for Cherri underwear/intimates. Pulls data from Semrush and GSC, identifies striking distance queries, clusters by intent, and outputs prioritized keyword lists with volume and difficulty metrics.
---

<purpose>

Find and prioritize keyword opportunities for Cherri's underwear/intimates e-commerce site by combining:
- **Semrush** data: Search volume, keyword difficulty, competitor rankings
- **GSC** data: Current rankings, impressions, CTR, striking distance queries
- **Intent analysis**: Transactional vs informational vs navigational

</purpose>

<intake>

**What type of keyword research do you need?**

1. **Striking distance audit** - Find queries ranking 4-20 with high impressions (quick wins)
2. **New keyword opportunities** - Discover untapped keywords in the underwear/intimates space
3. **Competitor keyword gap** - Find keywords competitors rank for but Cherri doesn't
4. **Content cluster mapping** - Group existing rankings into topic clusters
5. **Seasonal trend analysis** - Identify trending keywords for upcoming seasons

**Provide:**
- Cherri's domain (if not wearcherri.com)
- Target market (US, UK, etc.)
- Any specific product categories to focus on
- Competitor domains to analyze (optional)

</intake>

<workflow_striking_distance>

## Striking Distance Audit

**Goal:** Find queries ranking positions 4-20 with high impressions that could move to page 1.

### Step 1: Pull GSC Data

Query GSC for last 28 days:
- Filter: positions 4-20
- Sort by: impressions (descending)
- Limit: top 100 queries

### Step 2: Enrich with Semrush

For each query, pull from Semrush:
- Search volume (monthly)
- Keyword difficulty
- CPC (indicates commercial intent)
- SERP features present

### Step 3: Score Opportunities

Calculate opportunity score:
```
Score = (Impressions × Volume) / (Difficulty × (Position - 3))
```

Higher score = better opportunity

### Step 4: Categorize by Intent

| Intent | Signals | Priority |
|--------|---------|----------|
| Transactional | "buy", "shop", price terms, product names | Highest |
| Commercial Investigation | "best", "review", "vs", comparisons | High |
| Informational | "how to", "what is", guides | Medium |
| Navigational | Brand terms, "cherri underwear" | Monitor |

### Step 5: Output

Generate prioritized list with columns:
- Query
- Current Position
- Impressions (28d)
- Volume
- Difficulty
- Intent
- Opportunity Score
- Recommended Action

Save to: `research/keywords/striking-distance-YYYY-MM-DD.csv`

</workflow_striking_distance>

<workflow_new_keywords>

## New Keyword Discovery

**Goal:** Find untapped keywords in underwear/intimates space.

### Step 1: Seed Keywords

Start with category seeds:
- underwear, panties, bras, intimates
- sustainable underwear, organic cotton underwear
- comfortable underwear, everyday underwear
- women's underwear, men's underwear

### Step 2: Expand via Semrush

For each seed, pull:
- Related keywords
- Questions
- Long-tail variations
- Phrase match keywords

Filter for:
- Volume > 100/month
- Difficulty < 60
- Not already ranking (check GSC)

### Step 3: Cluster by Topic

Group keywords into clusters:
- Product types (bras, panties, boxers)
- Materials (cotton, bamboo, organic)
- Benefits (comfortable, sustainable, breathable)
- Occasions (everyday, special occasion, athletic)

### Step 4: Prioritize

Rank clusters by:
- Total volume potential
- Average difficulty
- Alignment with Cherri brand values
- Commercial intent

### Step 5: Output

Generate keyword opportunity report:
- Cluster name
- Total monthly volume
- Average difficulty
- Top 10 keywords in cluster
- Recommended content type (PDP, collection page, blog)

Save to: `research/keywords/opportunities-YYYY-MM-DD.csv`

</workflow_new_keywords>

<workflow_competitor_gap>

## Competitor Keyword Gap Analysis

**Goal:** Find valuable keywords competitors rank for that Cherri doesn't.

### Step 1: Define Competitors

Default competitors (adjust as needed):
- parade.com
- tommyjohn.com
- meundies.com
- cuup.com

### Step 2: Pull Competitor Keywords

From Semrush, for each competitor:
- Organic keywords (top 1000)
- Filter: positions 1-20

### Step 3: Compare to Cherri

Cross-reference with Cherri's rankings:
- Find keywords where competitors rank but Cherri doesn't
- Or where competitors rank significantly higher

### Step 4: Filter for Relevance

Remove keywords that are:
- Competitor brand terms
- Irrelevant products
- Very low volume (< 50)
- Very high difficulty (> 80)

### Step 5: Prioritize Gaps

Score gaps by:
```
Gap Score = Volume × (1 / Difficulty) × CompetitorCount
```

Where CompetitorCount = number of competitors ranking for this keyword

### Step 6: Output

Generate gap analysis:
- Keyword
- Volume
- Difficulty
- Which competitors rank
- Their positions
- Gap Score
- Content recommendation

Save to: `research/keywords/competitor-gap-YYYY-MM-DD.csv`

</workflow_competitor_gap>

<output_formats>

## Standard Output Columns

**Keyword List CSV:**
```
keyword,volume,difficulty,cpc,intent,current_position,impressions,ctr,opportunity_score,action
```

**Cluster Report:**
```
cluster_name,keyword_count,total_volume,avg_difficulty,top_keywords,content_type
```

**Gap Analysis:**
```
keyword,volume,difficulty,competitors_ranking,avg_competitor_position,gap_score,recommendation
```

</output_formats>

<best_practices>

## Keyword Research Best Practices

1. **Always verify data freshness** - GSC and Semrush data can lag
2. **Check for cannibalization** - Multiple pages targeting same keyword
3. **Consider search intent match** - Don't target informational keywords with product pages
4. **Account for seasonality** - Underwear searches may spike around holidays
5. **Monitor brand vs non-brand** - Track ratio over time
6. **Validate with actual SERPs** - Check what's ranking before recommending content type

</best_practices>

<quick_commands>

## Quick Commands

**Striking distance quick scan:**
"Find top 20 striking distance opportunities for Cherri"

**Competitor quick gap:**
"What keywords does Parade rank for that Cherri doesn't?"

**Topic cluster:**
"Create a keyword cluster around 'sustainable underwear'"

**Trend check:**
"What underwear keywords are trending up this month?"

</quick_commands>
