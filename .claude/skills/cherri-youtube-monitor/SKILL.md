---
name: cherri-youtube-monitor
description: Weekly YouTube community intelligence sweep using yt-dlp. Searches underwear-related topics, extracts video metadata, transcripts, and top comments. Produces a report with competitor mentions, sentiment analysis, creator intelligence, content ideas, and engagement opportunities.
allowed-tools: Bash, Read, Write, Glob, Task
user-invocable: true
---

# Cherri YouTube Community Monitor

Run weekly sweeps across YouTube to gather community intelligence about underwear discussions, competitor mentions, and content opportunities for Cherri.

**Engine:** yt-dlp (no API key required)
**Output:** `marketing/research/youtube/YYYY-MM-DD-weekly-report.md`

---

## Reference Data

### Junk Channel Blocklist

Channels matching these patterns should be excluded from results:

- Channels primarily about men's underwear (boxer briefs, men's fit reviews)
- Known NSFW try-on haul channels (lingerie try-on with suggestive thumbnails, "transparent" try-on)
- Spam/clickbait reupload channels (stolen content, AI voiceover compilations, keyword-stuffed titles)
- Channels with zero original commentary (pure affiliate slideshows)
- Fetish/kink content disguised as reviews

### Competitor Brand Categories

| Category | Brands |
|----------|--------|
| **Direct** (small brands, similar positioning) | La Coochie, Underdays, Fruity Booty, SpicyWear |
| **Adjacent** (different positioning, overlapping audience) | Huha, MeUndies, Panty Drop, Lively |
| **Closed** (former competitors, still discussed) | Parade |
| **Mainstream declining** (legacy brands losing trust) | Aerie, Victoria's Secret, Lane Bryant, Torrid |

Additional brands to scan for: Calvin Klein, ThirdLove, Skims, Bombas, Boody, TomboyX, Duluth Trading, Pact

### Common Video Schema

The normalized shape every video must conform to after analysis:

```json
{
  "title": "string",
  "url": "https://www.youtube.com/watch?v={id}",
  "channel": "string",
  "subscribers": "number or null",
  "upload_date": "YYYY-MM-DD",
  "views": "number",
  "likes": "number",
  "comment_count": "number",
  "duration_seconds": "number",
  "sentiment": "positive|negative|mixed|neutral",
  "brands_mentioned": "comma-separated string",
  "key_quote": "string (max 200 chars, from transcript or top comment)",
  "pain_points": "string (comma-separated)",
  "why_relevant": "string (one sentence)",
  "top_comments": [{"text": "string", "likes": "number"}],
  "transcript_snippet": "string (first 500 words)"
}
```

### Search Topics

Queries are organized into 3 tiers. Brand-specific queries pull the most relevant content on YouTube because the algorithm favors specific searches. Format queries target YouTube-native content types. Problem queries surface content about issues Cherri solves.

**IMPORTANT:** Never include "try on" in queries — this phrase is an NSFW magnet on YouTube and will surface lingerie/see-through haul content instead of genuine reviews.

**Tier A — Brand searches (5 queries):**

| # | Category | Query |
|---|----------|-------|
| 1 | Competitor: Aerie | `Aerie underwear review 2025 2026` |
| 2 | Competitor: Parade | `Parade underwear review quality` |
| 3 | Competitor: Skims | `Skims underwear review honest women` |
| 4 | Competitor: MeUndies | `MeUndies review women underwear` |
| 5 | Competitor: VS | `Victoria Secret underwear quality decline alternative` |

**Tier B — Format searches (4 queries):**

| # | Category | Query |
|---|----------|-------|
| 6 | Discovery: rankings | `best underwear brands 2025 2026 women ranking` |
| 7 | Discovery: tier lists | `underwear brand tier list women` |
| 8 | Discovery: reviews | `everyday underwear honest review women comfortable` |
| 9 | Discovery: comparisons | `underwear comparison women cotton comfort` |

**Tier C — Problem/need searches (3 queries):**

| # | Category | Query |
|---|----------|-------|
| 10 | Product: comfort/gusset | `comfortable underwear women wide gusset organic cotton` |
| 11 | Sensory: neurodivergent | `sensory friendly clothing underwear autism ADHD` |
| 12 | Product: plus size | `plus size underwear review women inclusive` |

---

## Step 1: Verify yt-dlp

Check that yt-dlp is installed and accessible:

```bash
if ! command -v yt-dlp &>/dev/null; then
  echo "ERROR: yt-dlp is not installed." >&2
  echo "Install with: brew install yt-dlp" >&2
  exit 1
fi
echo "yt-dlp version: $(yt-dlp --version)"
```

If yt-dlp is missing, tell the user to install it and stop.

## Step 2: Run 12 Topic Searches in Parallel

Dispatch 3 Bash subagents via the `Task` tool to run all 12 searches concurrently in 3 tiers. Each subagent runs its tier of queries sequentially (yt-dlp can rate-limit if hammered).

Record `search_start_time` before dispatching:

```bash
search_start_time=$(date +%s)
echo "Search started at $(date -r $search_start_time '+%Y-%m-%d %H:%M:%S')"
```

### 2.1: Dispatch 3 Search Subagents

Send a **single message** with 3 `Task` tool calls (all `subagent_type: "Bash"`) so they run in parallel.

Each subagent receives a prompt with:
1. Its list of queries (from the **Search Topics** table, one tier per subagent)
2. The output file path for its tier
3. Instructions to run each query sequentially via yt-dlp, tag results with the query number, and write JSONL output

**Subagent prompt template** (adapt per tier):

> Run these yt-dlp searches sequentially. **Before each query**, write a JSON boundary marker, then run the search:
>
> ```bash
> echo '{"__boundary":true,"query_num":N}' >> /tmp/yt-search-tier-{x}.jsonl
> timeout 60 yt-dlp "ytsearch15:{query}" \
>   --dump-json --no-warnings --no-download 2>/dev/null \
>   >> /tmp/yt-search-tier-{x}.jsonl
> ```
>
> Replace `N` with the query number from the Search Topics table (1-12).
>
> After each search, log: "Search {N}/12: {category} — found {count} results"
>
> If a search fails or times out, log the error and continue with the next query.
>
> Queries:
> {list each query with its number}

**Tier assignments:**

| Subagent | Tier | Queries | Output file |
|----------|------|---------|-------------|
| A | Brand searches | 1-5 | `/tmp/yt-search-tier-a.jsonl` |
| B | Format searches | 6-9 | `/tmp/yt-search-tier-b.jsonl` |
| C | Problem searches | 10-12 | `/tmp/yt-search-tier-c.jsonl` |

### 2.2: Merge and Extract Results

After all 3 subagents complete:

1. Record `search_end_time` and compute wall time:
   ```bash
   search_end_time=$(date +%s)
   wall_time=$((search_end_time - search_start_time))
   echo "Search completed in ${wall_time}s"
   ```

2. Read all 3 tier files (`/tmp/yt-search-tier-{a,b,c}.jsonl`). Each line is a raw yt-dlp JSON object.

3. For each JSON object, extract these fields:

| yt-dlp field | Description |
|--------------|-------------|
| `id` | YouTube video ID |
| `title` | Video title |
| `webpage_url` | Full YouTube URL |
| `channel` | Channel name |
| `channel_follower_count` | Subscriber count (may be null) |
| `upload_date` | Format YYYYMMDD — convert to YYYY-MM-DD |
| `view_count` | View count |
| `like_count` | Like count |
| `comment_count` | Comment count |
| `duration` | Duration in seconds |
| `description` | Video description (for brand/content scanning later) |

Tag each result with which topic number found it: `"search_queries": [N]` where N is the topic number from the Search Topics table. To determine N, parse each tier file line by line — when you encounter a `__boundary` line (`{"__boundary":true,"query_num":N}`), set the current query number to N. All subsequent video JSON objects belong to that query until the next boundary marker.

4. Collect ALL results into a single JSON array. Track the `raw_count` (total results before any dedup).

5. Write the combined array to `/tmp/youtube-monitor-search.json` using the Write tool.

6. Clean up tier files:
   ```bash
   rm -f /tmp/yt-search-tier-a.jsonl /tmp/yt-search-tier-b.jsonl /tmp/yt-search-tier-c.jsonl
   ```

7. Report summary:
   ```
   12 searches across 3 tiers. {raw_count} total videos found in {wall_time}s.
   ```

## Step 3: Deduplicate and Filter

Apply these filters **in order** to the raw results in `/tmp/youtube-monitor-search.json`. After each step, record how many videos remain for the funnel stats.

### 3.1: URL Dedup

Group videos by URL (`https://www.youtube.com/watch?v={id}`). The same video can appear in multiple topic searches.

When duplicates exist:
1. Merge the `search_queries` arrays from all copies (e.g., `[1, 4, 8]` means topics 1, 4, and 8 all found this video)
2. Keep the entry with the richer metadata — prefer the copy with the longer description and more complete fields

Record count after URL dedup.

### 3.2: Duration Filter

Remove videos shorter than 60 seconds (`duration < 60`). These are YouTube Shorts or teasers with no substantive content for analysis.

Record count after duration filter.

### 3.3: Age Filter

Remove videos uploaded more than 90 days ago. Convert `upload_date` (YYYY-MM-DD) and compare against today's date.

If `upload_date` is missing or null, **keep** the video — don't penalize missing data.

Record count after age filter.

### 3.4: Content Filter

Remove videos that are clearly off-topic for Cherri:

- **Men's underwear only** — Title or description contains "men's underwear", "boxer briefs", "men's boxers", or "jockstrap" with no women's underwear context
- **Non-English content** — The `language` field is present and not English (`en`)
- **Pure entertainment / no review content** — If NEITHER the title NOR description (case-insensitive) contains ANY term from this relevance list, remove the video:

  ```
  underwear, panties, bra, lingerie, knickers, briefs, thong, cotton,
  comfort, fabric, fit, sizing, clothing, fashion, haul, review, organic,
  gusset, waistband, sensory, intimate, loungewear, activewear
  ```

  This catches music videos, gaming content, and other entertainment that matched a search keyword by coincidence but has no actual clothing/underwear discussion.

Keep videos that mention men's and women's underwear together. Only remove when the **entire** video is off-topic.

Record count after content filter.

### 3.5: NSFW Filter

Remove videos whose title (case-insensitive) contains ANY of these terms:

```
see-through, see through, transparent lingerie, micro bikini,
transparent try, lingerie try-on, lingerie 4k, bikini try-on,
sheer try, no bra, no panties, 4k try on, revealing try on,
lingerie haul, sexy try on, underwear try on 4k
```

Also remove videos whose title contains "try on" AND whose channel name or description matches patterns in the **Junk Channel Blocklist** (see Reference Data). This catches NSFW try-on haul channels that use generic titles.

Record count after NSFW filter.

### 3.6: Record Pre-Enrichment Funnel Stats

Build a funnel object tracking video counts through each stage so far:

```json
{
  "raw_total": 150,
  "after_url_dedup": 98,
  "after_duration_filter": 85,
  "after_age_filter": 72,
  "after_content_filter": 65,
  "after_nsfw_filter": 62
}
```

This funnel is extended in Step 4 after the spam split and included in the final report's Search Stats section.

## Step 4: Enrich Top Videos, Then Split by Subscriber Threshold

Enrichment runs **before** the spam filter. This ensures small-creator videos with highly relevant content get transcripts and comments analyzed, instead of being silently discarded.

### 4.1: Rank and Select Top 30

Rank all NSFW-filtered videos (from Step 3.5) by `view_count * recency_weight` where:

| Upload age | `recency_weight` |
|------------|-------------------|
| < 7 days ago | 1.0 |
| 7-30 days ago | 0.7 |
| 30-90 days ago | 0.4 |

Compute `upload_age_days` from `upload_date` relative to today. Sort descending by `view_count * recency_weight`. Select the top 30.

If fewer than 30 videos remain after NSFW filtering, enrich all of them.

### 4.2: Fetch Comments

For each of the top 30 videos, fetch the top 20 comments sorted by likes:

```bash
timeout 30 yt-dlp --write-comments --no-download --dump-json \
  --extractor-args "youtube:max_comments=20,all,0;comment_sort=top" \
  "https://www.youtube.com/watch?v={id}" 2>/dev/null
```

The `--write-comments` flag embeds comments in the JSON output under the `comments` field. Each comment object has `text`, `like_count`, `author`, `timestamp`, and more.

Extract the top 20 comments (already limited by `max_comments=20`). For each comment, keep:
- `text` — Comment text
- `like_count` — Number of likes on this comment

If comments are disabled or unavailable for a video, note `"comments_disabled": true` and continue.

**Extractor-args format:** `youtube:max_comments=COUNT,all,REPLIES;comment_sort=SORT`. Setting replies to `0` skips reply threads (faster). Setting `comment_sort=top` sorts by most liked.

### 4.3: Fetch Transcript

For each of the top 30 videos, fetch auto-generated English captions:

```bash
timeout 30 yt-dlp --write-auto-subs --sub-lang en --sub-format vtt \
  --skip-download --no-warnings \
  -o "/tmp/yt-subs/%(id)s" \
  "https://www.youtube.com/watch?v={id}" 2>/dev/null
```

This saves the transcript as a VTT file at `/tmp/yt-subs/{id}.en.vtt`.

After downloading, clean the VTT to plaintext:

1. Strip the `WEBVTT` header line and any metadata lines
2. Remove timestamp lines (format: `HH:MM:SS.mmm --> HH:MM:SS.mmm`)
3. Remove cue numbers (standalone numbers on their own line)
4. Strip HTML tags (e.g., `<c>`, `</c>`, alignment tags)
5. Deduplicate overlapping lines — yt-dlp auto-subs often repeat phrases across cues. Keep only unique lines in sequence.
6. Truncate to the first **500 words**

Set the result as the `transcript_snippet` field on the video object.

If no auto-captions are available for a video, set `transcript_snippet` to null. Not all videos have captions (~40-50% do).

### 4.4: Error Handling

- Timeout each enrichment call at **30 seconds** (both comments and transcript)
- If comment fetch fails, keep the video but mark `"comments_error": true`
- If transcript fetch fails, keep the video but set `transcript_snippet` to null
- Log progress for each video:
  ```
  Enriching {N}/30: {title} — comments: {ok/fail}, transcript: {ok/fail}
  ```
- If a video is age-restricted or private, skip enrichment entirely and note why

### 4.5: Spam Split — Main Set vs. Sub-Threshold Set

After enrichment, split the enriched videos into two buckets based on subscriber count:

**Threshold:** 100 subscribers (`channel_follower_count < 100`)

**Relevance rescue:** Before assigning a video to the sub-threshold set, check if its title (case-insensitive) contains ANY of these underwear-review keywords:

```
underwear review, cotton underwear, organic underwear, panties review,
knickers review, gusset, sensory friendly underwear
```

If it matches, keep the video in the **main set** regardless of subscriber count. These are exactly the niche creators Cherri wants to find.

**Bucket assignment:**

| Condition | Bucket |
|-----------|--------|
| `channel_follower_count >= 100` OR null/missing | **Main set** |
| `channel_follower_count < 100` AND title matches a rescue keyword | **Main set** (rescued) |
| `channel_follower_count < 100` AND no rescue keyword match | **Sub-threshold set** |

Record counts: `main_set_count`, `sub_threshold_count`, `rescued_count`.

Update the funnel stats:

```json
{
  "raw_total": 150,
  "after_url_dedup": 98,
  "after_duration_filter": 85,
  "after_age_filter": 72,
  "after_content_filter": 65,
  "after_nsfw_filter": 62,
  "enriched": 30,
  "main_set": 25,
  "sub_threshold": 5,
  "rescued": 1
}
```

### 4.6: Write Enriched Results

Write the full enriched data to `/tmp/youtube-monitor-enriched.json` using the Write tool. The JSON should contain:

```json
{
  "main_set": [...],
  "sub_threshold": [...],
  "funnel": { ... }
}
```

Each video object includes:

- All fields from Step 2 (metadata from search)
- `top_comments` array (from 4.2)
- `transcript_snippet` string (from 4.3)
- `bucket` — `"main"` or `"sub_threshold"`
- Error flags if applicable (`comments_disabled`, `comments_error`)

Track and report enrichment stats:

```
Enrichment: {attempted} videos, {comments_ok} comments OK, {transcripts_ok} transcripts OK
Spam split: {main_set_count} main, {sub_threshold_count} sub-threshold, {rescued_count} rescued
```

## Step 5: Cherri Analysis

Analyze ALL enriched video data from `/tmp/youtube-monitor-enriched.json` — both the main set and sub-threshold set — for competitive intelligence, engagement opportunities, and content ideas.

### 5.1: Normalize to Common Video Schema

For each enriched video, build a **Common Video Schema** object (see Reference Data). The LLM (Claude) analyzes each video's title, description, transcript, and comments to determine:

- `sentiment` — Overall sentiment of the video + comments toward underwear. Use `positive` (praise/recommendation), `negative` (complaint/frustration), `mixed` (both), or `neutral` (informational/educational)
- `brands_mentioned` — Scan title, description, transcript text, AND comment text for all brands in the **Competitor Brand Categories** table (see Reference Data). Comma-separated string.
- `key_quote` — Most relevant quote (max 200 chars, no newlines). Prefer the highest-liked comment that mentions a pain point or brand opinion. Fall back to a relevant transcript excerpt.
- `pain_points` — Comma-separated list of comfort/fit/health issues discussed (e.g., "wedgies, narrow gusset, rolling waistband, UTI, chafing")
- `why_relevant` — One sentence on why this video matters for Cherri

After building all schema objects, write the array to `/tmp/youtube-monitor-schemas.json` using the Write tool. This intermediate artifact enables auditable analysis and programmatic week-over-week diffs. Include every enriched video (both main set and sub-threshold set).

### 5.2: Competitor Cross-Reference

Scan each video's `brands_mentioned` field for known competitors using the **Competitor Brand Categories** table (see Reference Data). Categorize each mention by its category (Direct, Adjacent, Closed, Mainstream declining).

Build a competitor mention summary: for each brand that appears, count how many videos mention it, note the prevailing sentiment (positive, negative, mixed, neutral), and distinguish between **creator mentions** (brand named in title/description/transcript) vs. **commenter mentions** (brand named in comments only). Highlight any brand-switching discussions where someone is leaving a competitor.

### 5.3: Engagement Opportunity Flags

Review each video and flag it as an **engagement opportunity** if ANY of these conditions are true:

1. **Creator asks for recommendations** — Video asks viewers what underwear they like/recommend (high-intent moment — comment section is where the action is)
2. **Negative competitor review** — Creator negatively reviews a competitor brand (brand-switching opportunity). Pay special attention to Parade, Aerie, and VS complaints — these are Cherri's most common switching sources.
3. **Cherri differentiator discussed as unmet need** — Comments or transcript discuss ANY of these Cherri-specific value props as something they wish existed or can't find:
   - Wide gusset / fuller coverage
   - Organic cotton / GOTS-certified materials
   - Inclusive sizing (especially XS-4XL range)
   - Everyday comfort (not lingerie, not special occasion)
   - No irritating tags, seams, or waistband rolling
4. **Sensory/neurodivergent discussion** — Video or comments discuss sensory sensitivity, texture issues, autism/ADHD and clothing comfort
5. **Brand comparison / tier list** — Creator ranks or compares underwear brands (opportunity for Cherri to be featured in future lists)
6. **Small creator partnership potential** — Creator has <50K subscribers, is reviewing underwear genuinely, and has an engaged audience (like-to-view ratio > 3%)

For each flagged video, note which condition(s) it matches and suggest a specific action:
- **Comment** — Leave a helpful (not salesy) comment addressing the need. Focus on the specific pain point (e.g., "wide gusset" or "organic cotton") rather than brand promotion.
- **Reach out** — DM/email the creator about a potential collaboration or product send
- **Create response content** — Make a Cherri video responding to this topic
- **Monitor** — Keep watching this creator/thread for developments

### 5.4: Relevance Prioritization

Rank all videos by relevance to Cherri using these criteria (in priority order):

1. **Cherri differentiator match** (highest weight) — Video discusses wide gussets, organic cotton, inclusive sizing, everyday comfort, or sensory-friendly underwear. These are Cherri's core selling points. A 60-day-old video about wide gussets is more valuable than a 3-day-old fashion trends video.
2. **Competitor brand discussion** — Video reviews or mentions a specific competitor brand from the **Competitor Brand Categories** table. Brand-switching conversations are high-intent.
3. **Recency** — Videos < 7 days old get a boost, but recency alone doesn't determine priority.
4. **Engagement quality** — Comments discussing real problems (fit issues, material complaints, brand frustrations) matter more than view count. A 5K-view video with 200 comments debating underwear brands is more valuable than a 500K-view fashion trends video.

Assign each video a priority tier: **High**, **Medium**, or **Low**. Sort by priority tier (High first), then by date (newest first within each tier).

**High** = Discusses Cherri differentiators OR reviews a direct competitor OR has active brand-switching discussion.
**Medium** = Adjacent content (fashion/comfort reviews, health content) with relevant comments.
**Low** = Tangentially related content worth monitoring but no immediate action needed.

### 5.5: Content Ideas

Flag videos that suggest content opportunities for Cherri. For each, note the content type and a brief angle:

- **Response video** — Creator covered a topic Cherri should respond to (e.g., "underwear that doesn't ride up" -> Cherri response showing wide gusset design)
- **Blog post** — Educational content inspired by video topic (e.g., video about UTIs from synthetic fabrics -> blog post on fabric science and vaginal health)
- **Collaboration** — Small-to-mid creator worth partnering with (genuine reviewer, engaged audience, aligns with Cherri values)
- **TikTok** — Short-form content idea from a trending topic or common question in comments
- **Product page copy** — Language, pain points, and phrases from comments that should appear on Cherri's product descriptions

Focus on videos with high engagement where community language reveals pain points Cherri solves.

### 5.6: Creator Intelligence

Identify notable creators from the enriched video set:

- **Repeat reviewers** — Creators with multiple videos in results (reviewing underwear regularly)
- **Competitor advocates** — Creators who promote a specific competitor brand
- **Collaboration targets** — Engaged audience (<100K subs), positive toward comfort/organic/inclusive values, genuine review style
- **Large monitors** — Big creators (>100K subs) covering the underwear/fashion space

For each notable creator, record:
- Channel name and subscriber count
- Average views across their videos in results
- Topics they cover
- Potential classification: "Collaboration target", "Monitor", or "Competitor advocate"

## Step 6: Week-over-Week Diff

Compare this week's results against the previous report to surface trends and track engagement windows.

### 6.1: Find Previous Report

Look for the most recent weekly report that is NOT the current output file. The current output file is `marketing/research/youtube/YYYY-MM-DD-weekly-report.md` (today's date). An earlier run on the same day counts as a valid comparison baseline — the new report will overwrite it.

```bash
today=$(date +%Y-%m-%d)
output_file="marketing/research/youtube/${today}-weekly-report.md"
ls -1 marketing/research/youtube/*-weekly-report.md 2>/dev/null | sort | grep -v "^${output_file}$" | tail -1
```

If the result is a file from today, that's fine — it's from an earlier run and should be used as the comparison.

### 6.2: If No Previous Report Exists

If no previous report is found, note in the final report:

> **Week-over-Week:** First report — no comparison available.

Skip the rest of Step 6 and proceed to report generation.

### 6.3: If Previous Report Exists

Read the previous report and extract the **Raw Video Index** table. Parse the table rows to build a lookup of `{ url: { title, channel, views, comments, date } }` for comparison.

### 6.4: Compute Diffs

Compare this week's analyzed video list against the previous report's video index:

- **New videos** — URLs in this week's results that do not appear in the previous report. These are newly discovered content.
- **Gained engagement** — URLs that appear in both reports where the `views` or `comment_count` increased. Note the delta (e.g., "views: 15,243 → 28,901").
- **Engagement windows closing** — Videos that appeared in the previous report's Engagement Opportunities section and are now more than 14 days old. These are running out of time for Cherri to engage.
- **New competitor mentions** — Brand names that appear in this week's `brands_mentioned` but did not appear anywhere in the previous report.
- **New creators** — Channel names appearing this week that weren't in the previous report.

### 6.5: Diff Summary

Build a summary section for the report with a table and sub-sections for each diff category (new videos, gained engagement, engagement windows closing, new competitor mentions, new creators).

## Step 7: Generate Report

Write the unified report to `marketing/research/youtube/YYYY-MM-DD-weekly-report.md` (using today's date).

Create the directory if it doesn't exist:

```bash
mkdir -p marketing/research/youtube
```

Use this EXACT template. Fill every section from the analysis in Steps 5 and 6. Every video reference in prose sections MUST use `[Video Title](url) (YYYY-MM-DD)`. Every table with videos MUST include a Date column.

````markdown
# YouTube Community Intelligence — Week of YYYY-MM-DD

## What Changed This Week

**Compared against:** [previous report filename] ([date])

| Metric | Count |
|--------|-------|
| New videos | X |
| Gained engagement | X |
| Engagement windows closing | X |
| New competitor mentions | X |
| New creators | X |

### New Videos
<!-- List of new video titles with URLs and dates, sorted by priority -->

### Gained Engagement
<!-- Videos with meaningful view/comment deltas since last week -->

### Engagement Windows Closing
<!-- Videos >14 days old that were flagged as opportunities last week -->

### New Competitor Mentions
<!-- Brand names newly appearing this week -->

### New Creators
<!-- Channel names appearing this week that weren't in last report -->

## Executive Summary
<!-- 3-5 bullet points: most actionable findings first -->

## Sentiment Snapshot

### What Creators/Viewers Love
<!-- Positive sentiment themes with video references -->

### What Creators/Viewers Hate
<!-- Negative sentiment themes with video references -->

### What People Wish Existed
<!-- Unmet needs and feature requests from comments -->

## Competitor Mentions

| Brand | Category | Videos | Sentiment | Source | Key Quote |
|-------|----------|--------|-----------|--------|-----------|

Source column values: "Creator" (brand named in title/description/transcript), "Commenter" (brand named in comments only), or "Both".

## Creator Intelligence

| Channel | Subscribers | Avg Views | Topics | Potential |
|---------|-------------|-----------|--------|-----------|

## Engagement Opportunities

| Video | Channel | Date | Why Relevant | Suggested Action |
|-------|---------|------|--------------|-----------------|

## Content Ideas

| Topic | Source Video | Date | Content Type |
|-------|-------------|------|--------------|

## Comment Highlights
<!-- Top quotes from video comments, grouped by theme:
     comfort/fit, health/hygiene, sizing, brand sentiment, sensory -->

## Sensory & Neurodivergent Discussions
<!-- Videos and comments about sensory sensitivity, texture issues,
     tag irritation, or neurodivergent underwear needs. Include video references. -->

## Search Stats

| Metric | Value |
|--------|-------|
| Topic searches | 12 |
| Raw videos found | X |
| After URL dedup | X |
| After duration filter | X |
| After age filter | X |
| After content filter | X |
| After NSFW filter | X |
| Videos enriched | X |
| Main set (≥100 subs) | X |
| Sub-threshold (<100 subs) | X |
| Rescued by keyword | X |
| Comments fetched | X/X OK |
| Transcripts fetched | X/X OK |
| Wall time | Xs |
| Cost | $0 |

## Raw Video Index

| # | Title | Channel | Views | Comments | Date | Priority | URL |
|---|-------|---------|-------|----------|------|----------|-----|

Sort by priority tier (High first), then by date (newest first).

## Notable Sub-Threshold

Small-creator videos (<100 subs) that were enriched with transcripts and comments. These often contain the most authentic, niche underwear reviews.

| # | Title | Channel | Subs | Views | Date | Priority | Why Notable |
|---|-------|---------|------|-------|------|----------|-------------|
````

Only include the "What Changed" section if a previous report exists. If this is the first report, replace with:

```markdown
## What Changed This Week

> First report — no comparison available.
```

## Step 8: Cleanup and Summarize

### 8.1: Delete Temp Files

Remove intermediate files written during the sweep:

```bash
rm -f /tmp/youtube-monitor-search.json \
      /tmp/youtube-monitor-enriched.json \
      /tmp/youtube-monitor-schemas.json
rm -rf /tmp/yt-subs/
```

### 8.2: Present Key Findings

After writing the report, present a summary to the user covering:

1. **What changed since last week** — New video count, engagement shifts, any closing engagement windows. If this is the first report, note that.
2. **Top 3 engagement opportunities** — Video title, channel, date, link, and a one-sentence angle for each. Use the format `[Video Title](url) (YYYY-MM-DD)`.
3. **Competitor mentions worth noting** — Any brand-switching signals, new competitor appearances, or sentiment shifts.
4. **Best content ideas** — Top 2-3 content opportunities with suggested format (response video, blog, TikTok, collaboration).
5. **Notable creators** — Top 2-3 collaboration targets or creators worth monitoring.
6. **Search stats** — Videos found, enrichment success rate, wall time, cost ($0).

End with the path to the full report:

> Full report: `marketing/research/youtube/YYYY-MM-DD-weekly-report.md`
