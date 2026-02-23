---
name: cherri-reddit-monitor
description: Weekly Reddit community intelligence sweep using 3 search backends (Exa keyword search, Parallel AI deep research, OpenAI agentic search). Dispatches selected sources in parallel, merges and deduplicates results, and generates a unified report with competitor mentions, engagement opportunities, and content ideas.
allowed-tools: Bash, ToolSearch, Read, Write, Glob
user-invocable: true
---

# Cherri Reddit Community Monitor

Run weekly sweeps across Reddit to gather community intelligence about underwear discussions, competitor mentions, and content opportunities for Cherri.

This skill orchestrates 3 search backends, each with different strengths:

| Backend | Method | Strengths | Cost |
|---------|--------|-----------|------|
| **Exa** | MCP keyword search (`mcp__exa__web_search_exa`) | Fast, precise keyword matching, 10 queries | ~$0 |
| **Parallel AI** | MCP Task Group (`createTaskGroup`), 4 research tasks with structured output | Autonomous exploration, pre-analyzed threads | ~$0.04 |
| **OpenAI** | Responses API with `web_search` tool on `gpt-5-mini` | Agentic multi-step search, verified citations | ~$2-4 |

Sources run in parallel. Results are merged into a single deduplicated report with cross-source overlap tracking.

**Output:** `marketing/research/reddit/YYYY-MM-DD-weekly-report.md`

---

## Reference Data

These definitions are referenced throughout the skill. Define once, use everywhere.

### Junk URL Blocklist

Remove any thread whose URL contains any of these strings:

- `r/MeUndies/best`
- `r/TOH_TryOnHauls`
- `business.reddit.com`
- `r/MensUnderwearGuide`
- `r/PantyReviews4Men`
- `r/malefashionadvice`
- `r/AskIndianMen`
- `r/bigmenfashionadvice`

### Competitor Brand Categories

| Category | Brands |
|----------|--------|
| **Direct** (small brands, similar positioning) | La Coochie, Underdays, Fruity Booty, SpicyWear |
| **Adjacent** (different positioning, overlapping audience) | Huha, MeUndies, Panty Drop, Lively |
| **Closed** (former competitors, still discussed) | Parade |
| **Mainstream declining** (legacy brands losing trust) | Aerie, Victoria's Secret, Lane Bryant, Torrid |

Additional brands to scan for: Calvin Klein, ThirdLove, Skims, Bombas, Boody, TomboyX, Duluth Trading, Pact

### Common Thread Schema

Every source normalizes threads to this shape before writing results:

```json
{
  "title": "string",
  "url": "string (canonical Reddit URL, no query params or trailing slashes)",
  "subreddit": "string (extracted from URL path /r/<subreddit>/)",
  "date": "YYYY-MM-DD",
  "score": "string",
  "num_comments": "string",
  "sentiment": "positive|negative|mixed|neutral",
  "brands_mentioned": "comma-separated string (scan for all Competitor Brand Categories above)",
  "key_quote": "string (max 200 chars, no newlines)",
  "pain_points": "string (comma-separated: wedgies, narrow gusset, rolling waistband, etc.)",
  "why_relevant": "string (one sentence on why this matters for Cherri)"
}
```

### Research Topics

| # | Topic | Focus | Keywords | Subreddits |
|---|-------|-------|----------|------------|
| 1 | Comfort & Fit | Wedgies, riding up, bunching, fit issues | comfortable underwear, breathable, fit, wedgies, front wedgies, bunching | r/femalefashionadvice, r/ABraThatFits, r/TheGirlSurvivalGuide, r/women, r/TrollXChromosomes |
| 2 | Health & Hygiene | UTIs, yeast infections, chafing, sweat, irritation | UTI, yeast infection, chafing, sweat, irritation, breathability | r/HealthyHooha, r/TheGirlSurvivalGuide, r/WomensHealth, r/nursing |
| 3 | Sensory & Neurodivergent | Texture, seams, tags, sensory processing | sensory friendly, autism, ADHD, texture, seam sensitivity | r/autism, r/ADHD, r/adhdwomen, r/AuDHDWomen, r/SensoryProcessing |
| 4 | Plus Size | Rolling waistbands, limited sizes, chafing | plus size, rolling waistband, size range, thigh chafing | r/PlusSize, r/PlusSizeFashion, r/FrugalFemaleFashion |
| 5 | Sustainability | Organic cotton, toxin-free, eco-conscious | organic cotton, sustainable, toxin free, eco-conscious | r/SustainableFashion, r/ethicalfashion, r/ConsciousConsumers, r/moderatelygranolamoms |
| 6 | Wide Gusset | Gusset width, coverage, placement complaints | wide gusset, extra coverage, gusset too short, narrow gusset | Any subreddit |
| 7 | Competitor Brands | Quality complaints, brand switching, comparisons | Parade, Huha, Aerie, VS, MeUndies, La Coochie, Underdays, Fruity Booty, SpicyWear | Any subreddit |
| 8 | Recommendations | General recs, "best underwear", gift buying | underwear recommendation, best brand, what underwear do you wear | Any subreddit |

---

## Step 1: Select Sources

Ask the user which sources to run. Default is all three.

> Which sources should I run?
> 1. **Exa** — keyword search via MCP (~$0, ~1 min)
> 2. **Parallel AI** — deep research via MCP Task Group (~$0.07, ~3 min)
> 3. **OpenAI** — agentic search via Responses API (~$2-4, ~10 min)
>
> Default: all three. Reply with numbers (e.g. "1,2") or press enter for all.

If the user specifies sources, run only those. If no response or "all", run all three.

## Step 2: Load API Keys

Load API keys and MCP tools for the selected sources.

**Exa selected:** No API key needed. Load the MCP tool with `ToolSearch` query `select:mcp__exa__web_search_exa`.

**Parallel AI selected:** No API key needed (MCP server handles auth). Load the MCP tools with `ToolSearch` query `+parallel-task`. This loads `createTaskGroup`, `getStatus`, and `getResultMarkdown`.

**OpenAI selected:** Load and validate the API key from `~/.config/cherri/.env`:

```bash
if [ -f ~/.config/cherri/.env ]; then
  OPENAI_API_KEY=$(grep '^OPENAI_API_KEY=' ~/.config/cherri/.env | cut -d= -f2 | tr -d '"'"'" | xargs)
  export OPENAI_API_KEY
fi

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "ERROR: OPENAI_API_KEY not found or empty in ~/.config/cherri/.env" >&2
  echo "Set OPENAI_API_KEY=sk-... in ~/.config/cherri/.env" >&2
  exit 1
fi
```

If a required key is missing or an MCP tool fails to load, skip that source, warn the user, and continue with the remaining sources. If no sources have valid credentials, stop and report the errors.

## Step 3a: Source: Exa

**Run inline** (not as a subagent). Exa uses MCP tools which are only available in the main agent context.

Record `exa_start_time` before starting (use `date +%s` or equivalent).

### 3a.1: Run Exa Searches

Run all 10 queries below in **two parallel batches of 5** using `mcp__exa__web_search_exa` (loaded in Step 2). Fire queries 1-5 simultaneously, then queries 6-10 simultaneously. For each query, pass:
- `numResults: 8`
- `livecrawl: "preferred"`
- `includeDomains: ["reddit.com"]`

**Note:** Exa may return non-Reddit URLs despite `includeDomains`. After collecting results, discard any URL that does not contain `reddit.com` before proceeding to dedup.

**Problem-based queries:**

1. `"comfortable underwear" OR "breathable underwear" women site:reddit.com`
2. `"underwear that doesn't ride up" OR "front wedgies" OR "wedgie proof" site:reddit.com`
3. `chafing OR UTI underwear OR "yeast infection" underwear OR "sweat" underwear women site:reddit.com`
4. `"plus size underwear" OR "underwear doesn't fit" OR "rolling waistband" site:reddit.com`

**Product/brand-based queries:**

5. `"wide gusset" OR "gusset underwear" OR "extra coverage underwear" site:reddit.com`
6. `"organic cotton underwear" OR "sustainable underwear" OR "toxin free" underwear site:reddit.com`
7. `Huha underwear OR "Parade underwear" OR underwear brand quality site:reddit.com`

**Discovery-based queries:**

8. `underwear recommendation women site:reddit.com`
9. `"sensory friendly underwear" OR "sensory issues clothing" OR "underwear texture" site:reddit.com`
10. `"best underwear" OR "underwear brand" women 2025 OR 2026 site:reddit.com` *(update years annually)*

Collect all results into a single list. Track the `raw_count` (total results before dedup/filtering).

### 3a.2: Deduplicate and Filter

Apply the **Junk URL Blocklist** (see Reference Data above) to remove recurring noise threads.

Then:
- Remove duplicate URLs across all queries
- Remove threads that are only about men's underwear, lingerie/sexy wear, or period underwear products
- Remove deleted posts with no body text in Exa's returned content

### 3a.3: Fetch Missing Metadata

Exa results often include `Score:` and `Time Posted (UTC):` in the returned text. Parse these when available. For threads missing score, comment count, or date, fetch the Reddit JSON API.

**`WebFetch` is blocked on reddit.com.** Use Bash with a single Python script (`urllib.request`) to batch-fetch all URLs that need metadata. Do NOT use a shell for-loop — large JSON responses cause piping failures.

Run this in Bash:

```python
#!/usr/bin/env python3
"""Fetch Reddit JSON metadata for URLs missing score/comments."""
import json
import socket
import sys
import time
import urllib.error
import urllib.request

urls = json.loads(sys.argv[1])  # list of reddit URLs
results = {}
errors = {"http": 0, "network": 0, "parse": 0}

for url in urls:
    clean = url.rstrip("/")
    json_url = clean + ".json"
    try:
        req = urllib.request.Request(
            json_url,
            headers={"User-Agent": "cherri-monitor/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            post = data[0]["data"]["children"][0]["data"]
            results[url] = {
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "created_utc": post.get("created_utc", 0),
                "title": post.get("title", ""),
                "subreddit": post.get("subreddit", ""),
            }
    except urllib.error.HTTPError as e:
        print(f"WARNING: HTTP {e.code} for {url}", file=sys.stderr)
        results[url] = {"error": f"HTTP {e.code}", "error_type": "http"}
        errors["http"] += 1
    except (urllib.error.URLError, socket.timeout) as e:
        print(f"WARNING: Network error for {url}: {e}", file=sys.stderr)
        results[url] = {"error": str(e), "error_type": "network"}
        errors["network"] += 1
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(
            f"WARNING: Parse error for {url}: {type(e).__name__}: {e}",
            file=sys.stderr,
        )
        results[url] = {"error": str(e), "error_type": "parse"}
        errors["parse"] += 1
    time.sleep(0.5)  # rate limit

total_errors = sum(errors.values())
if total_errors > 0:
    print(
        f"Metadata fetch: {len(urls) - total_errors}/{len(urls)} OK, "
        f"{errors['http']} HTTP, {errors['network']} network, "
        f"{errors['parse']} parse errors",
        file=sys.stderr,
    )

print(json.dumps(results))
```

Pass the list of URLs needing metadata as a JSON array in `sys.argv[1]`. Parse the printed JSON output to fill in missing fields. Threads with an `"error"` key in the metadata should be flagged in the report's Search Stats section (e.g. "3 URLs failed metadata fetch").

### 3a.4: Normalize to Common Schema

Build a thread list conforming to the **Common Thread Schema** (see Reference Data above).

For each thread:
- **title**: From Exa result title or Reddit JSON
- **url**: Canonical Reddit URL (strip query params, trailing slashes)
- **subreddit**: Extract from URL path (`/r/<subreddit>/`)
- **date**: Convert `created_utc` to `YYYY-MM-DD`, or parse `Time Posted (UTC):` from Exa text
- **score / num_comments**: From Exa text parsing or Reddit JSON. Convert to string.
- **sentiment**: Analyze the Exa-returned text content. Use `positive` (praise/recommendation), `negative` (complaint/frustration), `mixed` (both), or `neutral` (question/informational)
- **brands_mentioned**: Scan text for all brands in the **Competitor Brand Categories** table (see Reference Data)
- **key_quote**: Most relevant quote from the thread (max 200 chars, no newlines)
- **pain_points**: Comma-separated list of pain points mentioned (e.g. "wedgies, narrow gusset, rolling waistband")
- **why_relevant**: One sentence on why this thread matters for Cherri

### 3a.5: Write Results

Record `exa_end_time` and compute `wall_time_seconds = exa_end_time - exa_start_time`.

Write the results to `/tmp/reddit-monitor-exa.json`:

```json
{
  "source": "exa",
  "threads": [
    {
      "title": "...",
      "url": "...",
      "subreddit": "...",
      "date": "YYYY-MM-DD",
      "score": "...",
      "num_comments": "...",
      "sentiment": "...",
      "brands_mentioned": "...",
      "key_quote": "...",
      "pain_points": "...",
      "why_relevant": "..."
    }
  ],
  "search_stats": {
    "raw_count": 80,
    "search_queries": 10,
    "wall_time_seconds": 45,
    "estimated_cost": "~$0"
  }
}
```

Use `Write` tool to save the file. The merge step (later) reads from `/tmp/reddit-monitor-exa.json`.

## Step 3b: Source: Parallel AI

**Runs inline using MCP tools.** The `createTaskGroup` call fires all 4 research tasks asynchronously on Parallel's servers and returns immediately. Call it before starting Exa (Step 3a) so Parallel AI processes server-side while Exa runs inline. After Exa completes, poll for Parallel AI completion and retrieve results.

Record `parallel_start_time` before starting (use `date +%s`).

### 3b.1: Create Task Group

Call `mcp__parallel-task__createTaskGroup` with:

**inputs** — 4 topic objects:

```json
[
  {"topic": "Find Reddit threads from the last 30 days where women discuss underwear comfort problems (wedgies, front wedgies, riding up, bunching, fit issues) or ask for underwear recommendations (best brand, what underwear do you wear, gift buying). Include threads from r/femalefashionadvice, r/ABraThatFits, r/TheGirlSurvivalGuide, r/women, r/TrollXChromosomes, and any subreddit with recommendation threads. For each thread, note the title, URL, subreddit, date, upvotes, comment count, overall sentiment, any underwear brands mentioned, specific pain points discussed, and what criteria people prioritize."},
  {"topic": "Find Reddit threads from the last 30 days where women discuss underwear-related health issues (UTIs, yeast infections, chafing, sweat, irritation, breathability) or sensory/texture problems with underwear (seam sensitivity, tag irritation, fabric texture) — especially from neurodivergent communities. Include threads from r/HealthyHooha, r/WomensHealth, r/nursing, r/TheGirlSurvivalGuide, r/autism, r/ADHD, r/adhdwomen, r/AuDHDWomen, r/SensoryProcessing. For each thread, note the title, URL, subreddit, date, upvotes, comment count, sentiment, brands mentioned, and health/sensory concerns discussed."},
  {"topic": "Find Reddit threads from the last 30 days about plus size underwear problems (rolling waistbands, limited size ranges, thigh chafing), sustainable/organic cotton/toxin-free underwear, or wide gusset/extra coverage underwear and gusset-related complaints (narrow gussets, gusset too short, gusset placement). Include threads from r/PlusSize, r/PlusSizeFashion, r/FrugalFemaleFashion, r/SustainableFashion, r/ethicalfashion, r/ConsciousConsumers, r/moderatelygranolamoms, and any subreddit. For each thread, note the title, URL, subreddit, date, upvotes, comment count, sentiment, brands mentioned, and specific product concerns or praise."},
  {"topic": "Find Reddit threads from the last 30 days that mention these specific underwear brands: Parade, Huha, Aerie, Victoria's Secret, MeUndies, La Coochie, Underdays, Fruity Booty, SpicyWear, Panty Drop, Lively, Lane Bryant, Torrid. Focus on quality complaints, brand switching, brand recommendations, or brand comparisons. For each thread, note the title, URL, subreddit, date, upvotes, comment count, sentiment, which brands are mentioned and whether sentiment toward each is positive/negative/neutral."}
]
```

**output_type**: `"json"`

**output**: `"For each topic, return an object with: threads (array of objects, each with: title (exact Reddit thread title), url (full Reddit URL https://www.reddit.com/r/...), subreddit (name without r/ prefix), date (YYYY-MM-DD), score (upvote count as string), num_comments (comment count as string), sentiment (positive/negative/mixed/neutral), brands_mentioned (comma-separated string of underwear brands mentioned), key_quote (most relevant quote from thread, max 200 chars), pain_points (specific issues discussed), why_relevant (why this matters for a women's underwear brand focused on comfort, wide gussets, organic cotton, and inclusive sizing)) and topic_summary (2-3 sentence summary of current discussion)"`

**processor**: `"pro"`

**source_policy**: `{"include_domains": ["reddit.com"]}`

Store the returned task group ID (format: `tgrp_*`). **Do not stop or share a URL with the user** — this is an automated workflow. Continue immediately to Step 3c (fire OpenAI background bash) and then Step 3a (run Exa inline).

### 3b.2: Poll for Completion

After Exa (Step 3a) completes, poll using `mcp__parallel-task__getStatus` with the task group ID. If not all tasks are complete, wait 30 seconds and poll again. Continue when status shows all tasks completed, or after 15 minutes (whichever comes first).

### 3b.3: Retrieve Results

Call `mcp__parallel-task__getResultMarkdown` with the task group ID and `basis: "all"` to retrieve all 4 task results at once.

### 3b.4: Normalize to Common Schema

Parse the returned markdown to extract thread objects from each task's JSON output. Parallel AI returns results as markdown tables where JSON arrays are encoded inside table cells using `<br>` as line breaks (not actual newlines). To extract the data:

1. Replace all `<br>` with `\n` in the full result text
2. Also unescape HTML entities (`&amp;` → `&`, `&lt;` → `<`, `&gt;` → `>`, `&quot;` → `"`)
3. Use balanced-brace JSON extraction to find arrays (`[...]`) containing thread objects — scan for `[`, track brace/bracket depth, and attempt `json.loads()` on each balanced candidate
4. The format may vary between runs — sometimes results appear as fenced JSON code blocks instead of tables. Handle both formats.

Build a combined thread list where each thread conforms to the **Common Thread Schema** (see Reference Data above).

Record `parallel_end_time` and compute `wall_time_seconds`.

Write results to `/tmp/reddit-monitor-parallel.json`:

```json
{
  "source": "parallel",
  "threads": [...],
  "search_stats": {
    "raw_count": "<total threads before dedup>",
    "search_queries": 4,
    "wall_time_seconds": "<computed>",
    "estimated_cost": "~$0.04"
  }
}
```

Use the `Write` tool to save the file. The merge step (Step 4) reads from `/tmp/reddit-monitor-parallel.json`.

## Step 3c: Source: OpenAI

**Run as a background bash process.** Fire this after Parallel AI's `createTaskGroup` call (Step 3b.1) and before starting Exa (Step 3a) so all three run in parallel. OpenAI tasks take 2-10 minutes total and require no MCP tools, so they run entirely in a background Bash call.

The script fires 8 background requests to OpenAI's Responses API with `gpt-5-mini` and `web_search` tool (domain-filtered to `reddit.com`), polls until completion, extracts results, and normalizes to the common schema.

Record `openai_start_time=$(date +%s)` at the beginning of the script.

```bash
set -u

openai_start_time=$(date +%s)

# Step 3c.1: Fire 8 background requests
# Uses urllib.request instead of curl to avoid exposing API key in process table
cat > /tmp/reddit-monitor-openai-fire.py <<'PYEOF'
import json, os, sys, urllib.error, urllib.request

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

system_prompt = '''You are a Reddit research analyst. Search Reddit thoroughly for threads matching the user's topic from the last 30 days.

IMPORTANT INSTRUCTIONS:
1. You have a budget of 12 web searches. Plan your queries strategically — use specific, varied queries to maximize coverage within this limit.
2. Open and read promising threads to extract accurate metadata.
3. Focus on threads with real discussion (multiple comments), not empty posts.
4. Return your findings as a JSON object wrapped in \`\`\`json fences.

Return this exact JSON structure:
\`\`\`json
{
  \"threads\": [
    {
      \"title\": \"Exact thread title\",
      \"url\": \"https://www.reddit.com/r/...\",
      \"subreddit\": \"SubredditName\",
      \"date\": \"YYYY-MM-DD\",
      \"score\": \"number as string\",
      \"num_comments\": \"number as string\",
      \"sentiment\": \"positive|negative|mixed|neutral\",
      \"brands_mentioned\": \"comma-separated brand names or empty string\",
      \"key_quote\": \"Most relevant quote from thread or top comments (max 200 chars)\",
      \"pain_points\": \"Specific comfort, fit, health, or sizing issues discussed\",
      \"why_relevant\": \"Why this matters for a women's underwear brand focused on comfort, wide gussets, organic cotton, and inclusive sizing\"
    }
  ],
  \"topic_summary\": \"2-3 sentence summary of what people are discussing about this topic on Reddit right now\"
}
\`\`\`

Include EVERY relevant thread you find. Do not summarize or skip threads.'''

# For each topic in the Research Topics table, construct a detailed prompt
# asking the model to find Reddit threads matching that topic.
topics = [
    'Find Reddit threads from the last 30 days where women discuss underwear comfort problems — fit issues, wedgies, front wedgies, underwear riding up, or bunching. Include threads from subreddits like r/femalefashionadvice, r/ABraThatFits, r/TheGirlSurvivalGuide, r/women, r/TrollXChromosomes. For each thread, note the title, URL, subreddit, date, upvotes, comment count, overall sentiment, any underwear brands mentioned, and specific pain points discussed.',
    'Find Reddit threads from the last 30 days where women discuss underwear-related health issues — UTIs, yeast infections, chafing, sweat, irritation, or breathability. Include threads from subreddits like r/HealthyHooha, r/TheGirlSurvivalGuide, r/WomensHealth, r/nursing. For each thread, note the title, URL, subreddit, date, upvotes, comment count, sentiment, brands mentioned, and health concerns discussed.',
    'Find Reddit threads from the last 30 days about sensory-friendly underwear, sensory issues with clothing, or underwear texture problems — especially from neurodivergent communities (autism, ADHD, sensory processing). Include threads from r/autism, r/ADHD, r/adhdwomen, r/AuDHDWomen, r/SensoryProcessing. For each thread, note the title, URL, subreddit, date, upvotes, comment count, sentiment, brands mentioned, and specific sensory complaints.',
    'Find Reddit threads from the last 30 days about plus size underwear problems — underwear that doesn\\'t fit, rolling waistbands, limited size ranges, chafing at larger sizes. Include threads from r/PlusSize, r/PlusSizeFashion, r/FrugalFemaleFashion. For each thread, note the title, URL, subreddit, date, upvotes, comment count, sentiment, brands mentioned, and sizing frustrations.',
    'Find Reddit threads from the last 30 days about organic cotton underwear, sustainable underwear, toxin-free underwear, or eco-conscious underwear brands for women. Include threads from r/SustainableFashion, r/ethicalfashion, r/ConsciousConsumers, r/moderatelygranolamoms. For each thread, note the title, URL, subreddit, date, upvotes, comment count, sentiment, brands mentioned, and what sustainability features people value.',
    'Find Reddit threads from the last 30 days about wide gusset underwear, extra coverage underwear, or gusset-related complaints — narrow gussets, gusset too short, gusset placement. Include any subreddit. For each thread, note the title, URL, subreddit, date, upvotes, comment count, sentiment, brands mentioned, and gusset-specific complaints or praise.',
    'Find Reddit threads from the last 30 days that mention these specific underwear brands: Parade, Huha, Aerie, Victoria\\'s Secret, MeUndies, La Coochie, Underdays, Fruity Booty, SpicyWear, Panty Drop, Lively, Lane Bryant, Torrid. Focus on quality complaints, brand switching, brand recommendations, or brand comparisons. For each thread, note the title, URL, subreddit, date, upvotes, comment count, sentiment, which brands are mentioned and whether sentiment toward each is positive/negative/neutral.',
    'Find Reddit threads from the last 30 days where women ask for underwear recommendations or discuss which underwear brand is best. Include general recommendation threads, what underwear do you wear threads, and gift-buying threads. For each thread, note the title, URL, subreddit, date, upvotes, comment count, which brands are recommended most, and what criteria people prioritize (comfort, price, material, style).',
]

response_ids = []

for i, topic in enumerate(topics):
    payload = {
        'model': 'gpt-5-mini',
        'reasoning': {'effort': 'high'},
        'tools': [
            {
                'type': 'web_search',
                'search_context_size': 'low',
                'filters': {
                    'allowed_domains': ['reddit.com']
                }
            }
        ],
        'input': [
            {
                'role': 'developer',
                'content': [{'type': 'input_text', 'text': system_prompt}]
            },
            {
                'role': 'user',
                'content': [{'type': 'input_text', 'text': topic}]
            }
        ],
        'background': True,
        'max_tool_calls': 15
    }

    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        'https://api.openai.com/v1/responses',
        data=data,
        headers={
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp_http:
            resp = json.loads(resp_http.read())
        resp_id = resp.get('id', '')
        status = resp.get('status', 'unknown')
        if resp_id:
            response_ids.append(resp_id)
            print(f'Task {i+1}/8: {resp_id} (status: {status})')
        else:
            error = resp.get('error', {}).get('message', str(resp)[:200])
            print(f'Task {i+1}/8: FAILED — {error}', file=sys.stderr)
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        print(f'Task {i+1}/8: FAILED — HTTP {e.code}: {body}', file=sys.stderr)
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f'Task {i+1}/8: FAILED — {e}', file=sys.stderr)

if not response_ids:
    error_result = {
        'source': 'openai',
        'threads': [],
        'search_stats': {
            'raw_count': 0, 'search_queries': 0,
            'wall_time_seconds': 0, 'estimated_cost': '~\$0',
            'error': 'All 8 fire requests failed'
        }
    }
    with open('/tmp/reddit-monitor-openai.json', 'w') as f:
        json.dump(error_result, f, indent=2)
    print('ERROR: 0/8 requests fired — wrote error JSON', file=sys.stderr)
    sys.exit(1)

with open('/tmp/reddit-monitor-openai-ids.json', 'w') as f:
    json.dump(response_ids, f)

print(f'\nFired {len(response_ids)}/8 background requests')
PYEOF

if ! uv run python3 /tmp/reddit-monitor-openai-fire.py; then
    echo 'OpenAI Step 3c.1 (fire) failed — check /tmp/reddit-monitor-openai.json' >&2
    # Don't exit — the error JSON is already written for the merge step
fi

# Step 3c.2: Poll for completion (timeout 10 min)
# Consecutive-failure tracking: transient parse errors on one poll don't
# permanently mark a task as errored — only after 3 consecutive failures.
cat > /tmp/reddit-monitor-openai-poll.py <<'PYEOF'
import json, os, sys, time, urllib.error, urllib.request

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

with open('/tmp/reddit-monitor-openai-ids.json') as f:
    response_ids = json.load(f)

terminal_states = {'completed', 'failed', 'cancelled'}
consecutive_failures = {rid: 0 for rid in response_ids}
start = time.time()
timeout = 600

while True:
    statuses = {}
    for rid in response_ids:
        req = urllib.request.Request(
            f'https://api.openai.com/v1/responses/{rid}',
            headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp_http:
                resp = json.loads(resp_http.read())
            statuses[rid] = resp.get('status', 'unknown')
            consecutive_failures[rid] = 0
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError, OSError) as e:
            consecutive_failures[rid] += 1
            if consecutive_failures[rid] >= 3:
                statuses[rid] = 'error'
                print(f'  {rid}: 3 consecutive poll failures — marking errored', file=sys.stderr)
            else:
                statuses[rid] = 'poll_retry'

    completed = sum(1 for s in statuses.values() if s == 'completed')
    failed = sum(1 for s in statuses.values() if s in ('failed', 'cancelled', 'error'))
    in_progress = sum(1 for s in statuses.values() if s not in terminal_states and s != 'error')
    elapsed = int(time.time() - start)

    print(f'OpenAI: [{elapsed}s] completed={completed} in_progress={in_progress} failed={failed}')

    if all(s in terminal_states or s == 'error' for s in statuses.values()):
        print('All OpenAI tasks reached terminal state!')
        break

    if time.time() - start > timeout:
        timed_out = sum(1 for s in statuses.values() if s not in terminal_states and s != 'error')
        print(f'TIMEOUT after {timeout}s — {completed} completed, {timed_out} timed out')
        break

    time.sleep(15)
PYEOF

if ! uv run python3 /tmp/reddit-monitor-openai-poll.py; then
    echo 'OpenAI Step 3c.2 (poll) failed' >&2
fi

# Step 3c.3: Retrieve results and normalize to common schema
openai_end_time=$(date +%s)
openai_wall_time=$((openai_end_time - openai_start_time))

cat > /tmp/reddit-monitor-openai-retrieve.py <<'PYEOF'
import json, os, sys, urllib.error, urllib.request

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

with open('/tmp/reddit-monitor-openai-ids.json') as f:
    response_ids = json.load(f)

all_threads = []
raw_count = 0

# Skip-reason tracking
skip_reasons = {
    'parse_error': 0, 'not_completed': 0, 'no_output': 0,
    'no_json': 0, 'json_invalid': 0,
}
tasks_completed = 0
tasks_failed = 0

for i, rid in enumerate(response_ids):
    req = urllib.request.Request(
        f'https://api.openai.com/v1/responses/{rid}',
        headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp_http:
            resp = json.loads(resp_http.read())
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f'Task {i+1}: Failed to fetch response: {e}', file=sys.stderr)
        skip_reasons['parse_error'] += 1
        tasks_failed += 1
        continue

    status = resp.get('status', 'unknown')
    if status != 'completed':
        print(f'Task {i+1}: Status is {status} — skipping')
        skip_reasons['not_completed'] += 1
        if status in ('failed', 'cancelled'):
            tasks_failed += 1
        continue

    tasks_completed += 1

    # Extract output text from the output array (NOT output_text,
    # which is empty for background responses)
    output_text = ''
    citation_urls = set()
    for item in resp.get('output', []):
        if item.get('type') == 'message':
            for content_item in item.get('content', []):
                if content_item.get('type') == 'output_text':
                    output_text = content_item.get('text', '')
                for ann in content_item.get('annotations', []):
                    if ann.get('type') == 'url_citation':
                        citation_urls.add(ann.get('url', ''))

    if not output_text:
        print(f'Task {i+1}: No output text found — skipping')
        skip_reasons['no_output'] += 1
        continue

    # Parse JSON using balanced-brace extraction
    # Finds the first valid JSON object containing 'threads'
    def extract_json_objects(text):
        results = []
        for start_idx in range(len(text)):
            if text[start_idx] != '{':
                continue
            depth = 0
            for end_idx in range(start_idx, len(text)):
                if text[end_idx] == '{':
                    depth += 1
                elif text[end_idx] == '}':
                    depth -= 1
                if depth == 0:
                    candidate = text[start_idx:end_idx + 1]
                    try:
                        obj = json.loads(candidate)
                        if 'threads' in obj:
                            return obj
                    except json.JSONDecodeError:
                        pass
                    break
        return None

    parsed = extract_json_objects(output_text)

    if parsed is None:
        print(f'Task {i+1}: No valid JSON with threads found — skipping')
        skip_reasons['no_json'] += 1
        continue

    threads = parsed.get('threads', [])
    raw_count += len(threads)

    # Cross-reference thread URLs with verified citations
    for thread in threads:
        thread['url_verified'] = thread.get('url', '') in citation_urls

    all_threads.extend(threads)
    print(f'Task {i+1}: {len(threads)} threads ({len(citation_urls)} verified URLs)')

wall_time = int(sys.argv[1])
timed_out = wall_time >= 600

result = {
    'source': 'openai',
    'threads': all_threads,
    'search_stats': {
        'raw_count': raw_count,
        'search_queries': 8,
        'wall_time_seconds': wall_time,
        'estimated_cost': '~\$2-4',
        'tasks_completed': tasks_completed,
        'tasks_failed': tasks_failed,
        'tasks_timed_out': len(response_ids) - tasks_completed - tasks_failed,
        'timed_out': timed_out,
        'skip_reasons': skip_reasons,
    }
}

with open('/tmp/reddit-monitor-openai.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f'OpenAI: {raw_count} raw threads written to /tmp/reddit-monitor-openai.json')
if any(v > 0 for v in skip_reasons.values()):
    print(f'  Skip reasons: {json.dumps(skip_reasons)}')
PYEOF

if ! uv run python3 /tmp/reddit-monitor-openai-retrieve.py "$openai_wall_time"; then
    echo 'OpenAI Step 3c.3 (retrieve) failed' >&2
    # Write minimal error JSON if retrieval script itself crashed
    if [ ! -f /tmp/reddit-monitor-openai.json ]; then
        echo '{"source":"openai","threads":[],"search_stats":{"error":"retrieval script crashed"}}' > /tmp/reddit-monitor-openai.json
    fi
fi

# Cleanup temp files
rm -f /tmp/reddit-monitor-openai-ids.json \
      /tmp/reddit-monitor-openai-fire.py \
      /tmp/reddit-monitor-openai-poll.py \
      /tmp/reddit-monitor-openai-retrieve.py
echo "OpenAI source complete (${openai_wall_time}s wall time)"
```

The entire script above runs as a single background Bash call. The orchestrator fires it alongside Parallel AI (Step 3b) before starting Exa (Step 3a), then collects the output file `/tmp/reddit-monitor-openai.json` after all sources finish. The merge step (Step 4) reads from this file.

## Step 4: Merge and Deduplicate

After all selected sources finish, merge their results into a single deduplicated thread list.

### 4.1: Load Source Results

Read whichever `/tmp/reddit-monitor-{source}.json` files exist. Only sources the user selected (and that completed successfully) will have files. Check for:

- `/tmp/reddit-monitor-exa.json`
- `/tmp/reddit-monitor-parallel.json`
- `/tmp/reddit-monitor-openai.json`

For each file that exists, parse the JSON and extract the `threads` array. Tag every thread with its source name (e.g. `"source": "exa"`). Combine all threads into a single list.

**Check for missing sources:** Compare found source files against the user's source selection from Step 1. If a selected source has no file, warn the user: "WARNING: {source} backend produced no results — check logs for errors." Include this warning in the report's Search Stats section.

Record the **raw total** before any dedup: sum of all threads across all source files.

### 4.1.5: Enrich Missing Metadata (All Sources)

Parallel AI and OpenAI threads often have `num_comments` of `"0"` or empty because those backends don't reliably return comment counts. Before entering the dedup pipeline, enrich these threads with real Reddit metadata.

1. Collect all thread URLs from Parallel AI and OpenAI results where `num_comments` is `"0"`, `""`, or missing
2. Also collect threads from any source where `score` is `"0"`, `""`, or missing
3. Batch-fetch their Reddit JSON metadata using the same Python script from Step 3a.3 (the `urllib.request` script that fetches `{url}.json`)
4. For each successful fetch, update the thread object's `score`, `num_comments`, and `date` with the fetched values
5. Threads that fail metadata fetch (HTTP errors, rate limits, timeouts) should keep their original values — do NOT set them to `"0"`

This ensures the zero-comment filter in Step E only removes threads **confirmed** to have zero comments, rather than threads where the backend simply didn't return metadata.

### 4.2: Dedup Pipeline

Apply these dedup/filter steps **in order**. After each step, record how many threads remain for the funnel stats.

#### Step A — URL Dedup

Group threads by canonical URL (strip query params, trailing slashes, normalize `www.reddit.com` vs `reddit.com`). When the same URL appears from multiple sources:

1. Keep the entry with the most detail — longer `key_quote` plus more items in `brands_mentioned`
2. Merge the `sources` arrays so the surviving entry records all backends that found it

Record count after URL dedup.

#### Step B — Title Similarity Dedup

Detect crossposts and reposts that have different URLs but near-identical titles. Compare titles case-insensitively after stripping leading/trailing whitespace. If two threads have titles with >90% character overlap (or one title is a substring of the other), keep the one with the higher `score` (fall back to higher `num_comments`). Merge `sources` arrays.

Record count after title dedup.

#### Step C — Junk URL Filter

Apply the **Junk URL Blocklist** (see Reference Data above).

Record count after junk URL filter.

#### Step D — Content Filter

Remove threads that are **only** about:

- Men's underwear (boxer briefs, men's boxers, jockstraps, etc. with no women's underwear discussion)
- Lingerie or sexy wear (teddies, babydolls, garter belts — not everyday underwear)
- Period underwear products specifically (Thinx, Knix period line, Saalt — unless the thread also discusses everyday comfort underwear)

Keep threads that mention these topics alongside general women's underwear discussion. Only remove threads where the **entire** discussion is off-topic for Cherri.

Record count after content filter.

#### Step E — Zero-Comment Filter

Remove threads where `num_comments` is `"0"` **after metadata enrichment** (Step 4.1.5). Only remove threads confirmed to have zero comments — threads that failed metadata fetch (HTTP errors, rate limits) should be kept rather than filtered, since their `"0"` value may be a backend artifact rather than a true zero.

Record count after zero-comment filter.

### 4.3: Build Merged Thread List

For each surviving thread, ensure it has a `sources` field — a JSON array of strings indicating which backends found it (e.g. `["exa", "parallel"]`, `["openai"]`, `["exa", "parallel", "openai"]`).

### 4.4: Record Funnel Stats

Build a funnel object tracking thread counts through each stage:

```json
{
  "raw_total": 185,
  "after_url_dedup": 142,
  "after_title_dedup": 128,
  "after_junk_filter": 119,
  "after_content_filter": 105,
  "after_zero_comment_filter": 87,
  "final": 87
}
```

`final` equals `after_zero_comment_filter`. This funnel is included in the final report.

## Step 5: Cherri Analysis

Analyze the merged thread list for competitive intelligence, engagement opportunities, and content ideas.

### 5.1: Competitor Cross-Reference

Scan each thread's `brands_mentioned` field for known competitors using the **Competitor Brand Categories** table (see Reference Data above). Categorize each mention by its category (Direct, Adjacent, Closed, Mainstream declining).

Build a competitor mention summary: for each brand that appears, count how many threads mention it and note the prevailing sentiment (positive, negative, mixed, neutral). Highlight any brand-switching threads where someone is leaving a competitor and looking for alternatives.

### 5.2: Engagement Opportunity Flags

Review each thread and flag it as an **engagement opportunity** if ANY of these conditions are true:

1. **Recommendation request with no clear winner** — Someone asking for underwear recommendations and the comments have no dominant brand consensus
2. **Narrow gusset frustration** — Someone frustrated with narrow gussets, short gussets, or gusset placement issues (direct Cherri value prop)
3. **Neurodivergent seeking sensory-friendly** — Neurodivergent person seeking sensory-friendly underwear (seam sensitivity, tag irritation, texture issues)
4. **Plus size fit problems** — Plus size person unable to find underwear that fits (rolling waistbands, limited size range, thigh chafing)
5. **Competitor dissatisfaction** — Someone dissatisfied with a competitor brand, especially Parade (closed), Aerie (quality decline), or Victoria's Secret (sizing issues)

For each flagged thread, note which condition(s) it matches and draft a one-sentence engagement angle describing how Cherri could contribute value to the conversation (not a sales pitch — genuine helpfulness).

### 5.3: Cherri Relevance Prioritization

Rank all threads by relevance to Cherri using these criteria (in priority order):

1. **Recency** — Threads less than 7 days old get highest priority. Threads 7-14 days old get medium. Older threads get low.
2. **Thread activity** — Higher `num_comments` and `score` indicate more active discussion
3. **Direct value prop match** — Thread discusses wide gussets, organic cotton, inclusive sizing, or everyday comfort (Cherri's core differentiators)
4. **Competitor dissatisfaction** — Thread contains negative sentiment toward a competitor, indicating potential brand-switchers

Assign each thread a priority tier: **High**, **Medium**, or **Low**. Sort the final thread list by priority tier (High first), then by date (newest first within each tier).

### 5.4: Content Ideas

Flag threads that suggest content opportunities for Cherri. For each flagged thread, note the content type and a brief angle:

- **Blog post** — Educational content about underwear fit, fabric science, health impacts, or buying guides. Example angle: "Thread about UTIs from synthetic underwear → blog post on how fabric choice affects vaginal health"
- **TikTok** — Short-form explainer, myth-busting, or response video. Example angle: "Thread about front wedgies → TikTok showing how gusset width affects fit"
- **Product page copy** — Language, pain points, and phrases real customers use that should appear on Cherri's product pages. Example angle: "Thread uses phrase 'underwear that stays put' → add to product description"

Focus on threads with high engagement (many comments, high score) where the community language reveals pain points that Cherri solves.

## Step 6: Week-over-Week Diff

Compare this week's results against the previous report to surface trends and track engagement windows.

### 6.1: Find Previous Report

Look for the most recent weekly report, excluding today's:

```bash
ls -1 marketing/research/reddit/*-weekly-report.md 2>/dev/null | sort | tail -1
```

If this returns a file with today's date, exclude it and take the next most recent:

```bash
today=$(date +%Y-%m-%d)
ls -1 marketing/research/reddit/*-weekly-report.md 2>/dev/null | sort | grep -v "$today" | tail -1
```

### 6.2: If No Previous Report Exists

If no previous report is found, note in the final report:

> **Week-over-Week:** First report — no comparison available.

Skip the rest of Step 6 and proceed to report generation.

### 6.3: If Previous Report Exists

Read the previous report and extract the Raw Thread Index table. This table contains URLs, scores, comment counts, and dates from the prior week.

Parse the table rows to build a lookup of `{ url: { score, num_comments, date } }` for comparison.

### 6.4: Compute Diffs

Compare this week's merged thread list against the previous report's thread index:

**New threads** — URLs in this week's results that do not appear in the previous report. These are newly discovered discussions.

**Gained engagement** — URLs that appear in both reports where the `score` or `num_comments` increased. Note the delta (e.g. "score: 45 → 89, comments: 12 → 31").

**Engagement window closing** — Threads that appeared in the previous report's Engagement Opportunities section and are now more than 14 days old. These are running out of time for Cherri to participate.

**New competitor mentions** — Brand names that appear in this week's `brands_mentioned` but did not appear anywhere in the previous report. These indicate new competitive activity.

### 6.5: Diff Summary

Build a summary section for the final report:

```markdown
## Week-over-Week Changes

**Compared against:** [previous report filename] ([date])

| Metric | Count |
|--------|-------|
| New threads | X |
| Gained engagement | X |
| Engagement windows closing | X |
| New competitor mentions | X |

### New Threads
[List of new thread titles with URLs, sorted by priority]

### Gained Engagement
[List of threads with score/comment deltas]

### Engagement Windows Closing
[List of threads >14 days old that were flagged as opportunities last week]

### New Competitor Mentions
[List of brand names newly appearing this week]
```

## Step 7: Generate Report

Write the unified report to `marketing/research/reddit/YYYY-MM-DD-weekly-report.md` (using today's date).

Create the directory if it doesn't exist:

```bash
mkdir -p marketing/research/reddit
```

Use the following template. Fill every section from the analysis in Steps 5 and 6. Every thread reference in prose sections MUST use `[Thread Title](url) (YYYY-MM-DD)`. Every table with threads MUST include a Date column.

````markdown
# Reddit Community Intelligence — Week of YYYY-MM-DD

## What Changed This Week

**Compared against:** [previous report filename] ([date])

| Metric | Count |
|--------|-------|
| New threads | X |
| Gained engagement | X |
| Engagement windows closing | X |
| New competitor mentions | X |

### New Threads
<!-- List of new thread titles with URLs and dates, sorted by priority -->

### Gained Engagement
<!-- Threads with meaningful score/comment deltas since last week -->

### Engagement Windows Closing
<!-- Threads >14 days old that were flagged as opportunities last week -->

### New Competitor Mentions
<!-- Brand names newly appearing this week -->

## Executive Summary
<!-- 3-5 bullet points: most actionable findings first -->

## Sentiment Snapshot

### What People Love
<!-- Positive sentiment themes with thread references -->

### What People Hate
<!-- Negative sentiment themes with thread references -->

### What People Wish Existed
<!-- Unmet needs and feature requests with thread references -->

## Competitor Mentions

| Brand | Thread | Date | Sentiment | Key Quote |
|-------|--------|------|-----------|-----------|

## Engagement Opportunities

| Thread | Subreddit | Date | Why It's Relevant | Suggested Angle |
|--------|-----------|------|-------------------|-----------------|

## Content Ideas

| Question/Topic | Source Thread | Date | Content Type |
|----------------|--------------|------|--------------|

## Sensory & Neurodivergent Discussions
<!-- Threads about sensory sensitivity, texture issues, tag irritation,
     or neurodivergent underwear needs. Include thread references. -->

## Search Stats

| Source | Threads Found | Searches | Wall Time | Cost |
|--------|--------------|----------|-----------|------|
| Exa | — | — | — | — |
| Parallel AI | — | — | — | — |
| OpenAI | — | — | — | — |
| **Merged** | **X unique** | — | — | **~$X.XX** |

Dedup funnel: X raw → X URL dedup → X filtered → **X final**
Cross-source overlap: X threads found by 2+ sources

Only include rows for sources that were actually run. Fill in real
numbers from each source's execution output:
- **Exa:** thread count from Step 3a, search count = number of queries,
  wall time from bash timing, cost ~$0.
- **Parallel AI:** thread count from Step 3b, searches = number of
  tasks, wall time from polling duration, cost from API response.
- **OpenAI:** thread count from Step 3c, searches = total
  `web_search_call` annotations across all queries, wall time from
  bash timing, cost from usage response.
- **Merged:** unique thread count after dedup (Step 4), total cost =
  sum of per-source costs.

## Raw Thread Index

| # | Title | Subreddit | Score | Comments | Date | Sources | URL |
|---|-------|-----------|-------|----------|------|---------|-----|

Sort by priority tier (High first), then by date (newest first).
The **Sources** column shows which backends found each thread
(e.g. "exa", "exa, parallel", "openai, parallel").
````

## Step 8: Cleanup and Summarize

### 8.1: Delete Temp Files

Remove intermediate JSON files written during the sweep:

```bash
rm -f /tmp/reddit-monitor-exa.json \
      /tmp/reddit-monitor-parallel.json \
      /tmp/reddit-monitor-openai.json
```

### 8.2: Present Key Findings

After writing the report, present a summary to the user covering:

1. **What changed since last week** — New thread count, engagement
   shifts, any closing engagement windows.
2. **Top 3 engagement opportunities** — Thread title, subreddit, date,
   link, and a one-sentence angle for each. Use the format
   `[Thread Title](url) (YYYY-MM-DD)`.
3. **Competitor mentions worth noting** — Any brand-switching signals,
   new competitor appearances, or sentiment shifts.
4. **Best content ideas** — Top 2-3 content opportunities with
   suggested format (blog, TikTok, product page copy).
5. **Per-source stats and total cost** — Threads found per source,
   dedup funnel, and total cost for the run.

End with the path to the full report:

> Full report: `marketing/research/reddit/YYYY-MM-DD-weekly-report.md`
