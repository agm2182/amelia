---
name: cherri-reddit-monitor-30days
description: Monitor Reddit for underwear discussions, competitor mentions, sensory-friendly conversations, and content ideas. Uses last30days engine for search. Produces weekly intelligence reports.
allowed-tools: Bash, Read, Write, Glob, ToolSearch
user-invocable: true
---

# Cherri Reddit Community Monitor (last30days)

Run weekly sweeps across Reddit using the `last30days.py` search engine. This skill is a single-source variant of `/cherri-reddit-monitor` — it uses the same analysis workflow but with one search backend instead of three.

**Engine:** last30days.py (`--sources=reddit --emit=compact`)
**Output:** `marketing/research/reddit/YYYY-MM-DD-weekly-report.md`

## Step 1: Locate last30days.py

Find the last30days research engine. Check these paths in order:

```bash
set -euo pipefail
SKILL_ROOT=""
for dir in \
  ".claude/skills/last30days" \
  "$HOME/.claude/skills/last30days"; do
  [ -n "$dir" ] && [ -f "$dir/scripts/last30days.py" ] && SKILL_ROOT="$dir" && break
done

if [ -z "${SKILL_ROOT:-}" ]; then
  echo "ERROR: last30days skill not found. Expected at .claude/skills/last30days/." >&2
  exit 1
fi
echo "Found last30days at: ${SKILL_ROOT}"
```

If not found, tell the user: "The last30days skill is required. Install it at `.claude/skills/last30days/`. As a fallback, you can use `/cherri-reddit-monitor` which includes Exa, Parallel AI, and OpenAI search backends."

## Step 2: Run 8 Topic Searches

Run each topic search **sequentially** using `last30days.py`. Each call uses `--sources=reddit --emit=compact` and a Bash timeout of 300000ms (5 minutes).

**CRITICAL: Run each search in the FOREGROUND. Read the ENTIRE output of each search — it contains scored, enriched Reddit threads with engagement metrics and comment insights.**

For each of the 8 topics below, run:

```bash
uv run python3 "${SKILL_ROOT}/scripts/last30days.py" "TOPIC" --sources=reddit --emit=compact
```

**The 8 topics:**

1. `comfortable underwear fit wedgies women`
2. `underwear UTI yeast infection chafing sweat women`
3. `sensory friendly underwear autism ADHD`
4. `plus size underwear fit rolling waistband`
5. `organic cotton sustainable underwear women`
6. `wide gusset underwear coverage`
7. `Parade underwear Huha Aerie quality decline`
8. `women's underwear recommendations best brand`

After each search completes, collect all Reddit thread items from the output. Each item includes:
- **ID and score** (weighted: relevance 0.45 + recency 0.25 + engagement 0.30)
- **Subreddit, title, URL, date**
- **Engagement metrics** (upvotes, comments)
- **Comment insights** (top comment excerpts)
- **Why it's relevant** (from the search engine)

Track succeeded and failed topic counts. If a topic search times out or fails, log: "Topic {N} ({keywords}) failed: {error}". Continue with the remaining topics. After all 8 topics, report: "{succeeded}/8 topic searches succeeded, {failed}/8 failed." If 0/8 succeeded, stop and report the error.

## Steps 3–7: Analysis and Reporting

Follow the analysis and reporting workflow from `/cherri-reddit-monitor` starting at **Step 4 (Merge and Deduplicate)**. Use the same:

- **Junk URL Blocklist** (Reference Data in `/cherri-reddit-monitor`)
- **Content filter** (men's underwear, lingerie, period underwear)
- **Zero-comment filter**
- **Competitor Brand Categories** cross-reference
- **Engagement Opportunity Flags** (5 conditions)
- **Cherri Relevance Prioritization** (recency → activity → value prop → competitor dissatisfaction)
- **Content Ideas** flagging (blog, TikTok, product page copy)
- **Week-over-Week Diff** (find previous report, compute new/gained/closing/competitor changes)
- **Report template** (same markdown structure)

The only difference: the Search Stats section shows a single source (last30days) instead of multiple backends. Format as:

```
8 topic searches → {raw} raw threads → {deduped} after URL dedup → {filtered} after filtering → **{final} unique threads**
```

## Step 8: Summarize

After saving the report, present the key findings to the user:
- What changed since last week (or note this is the first report)
- Top 3 engagement opportunities (with dates — flag if window is closing)
- Competitor mentions worth noting
- Best content ideas
- Anything surprising or new
