---
name: last30days
description: "Research a topic from the last 30 days. Also triggered by 'last30'. Sources: Reddit, X, YouTube, web. Become an expert and write copy-paste-ready prompts."
argument-hint: 'last30 AI video tools, last30 best project management tools'
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch, ToolSearch
user-invocable: true
disable-model-invocation: true
---

# last30days: Research Any Topic from the Last 30 Days

Research ANY topic across Reddit, X, YouTube, and the web. Surface what people are actually discussing, recommending, and debating right now.

## CRITICAL: Parse User Intent

Before doing anything, parse the user's input for:

1. **TOPIC**: What they want to learn about
2. **TARGET TOOL** (if specified): Where they'll use the prompts (e.g., "ChatGPT", "Midjourney")
3. **QUERY TYPE**:
   - **PROMPTING** - "X prompts", "prompting for X" - learn techniques, get copy-paste prompts
   - **RECOMMENDATIONS** - "best X", "top X", "what X should I use" - a LIST of specific things
   - **NEWS** - "what's happening with X", "X news" - current events/updates
   - **GENERAL** - anything else - broad understanding of the topic

Common patterns:
- `[topic] for [tool]` → TOOL IS SPECIFIED
- `[topic] prompts for [tool]` → TOOL IS SPECIFIED
- Just `[topic]` → TOOL NOT SPECIFIED, that's OK
- "best [topic]" or "top [topic]" → QUERY_TYPE = RECOMMENDATIONS

**Do NOT ask about target tool before research.** If not specified, research first, then ask after.

**Display your parsing:**
```
I'll research {TOPIC} across Reddit, X, and the web to find what's been discussed in the last 30 days.

Parsed intent:
- TOPIC = {TOPIC}
- TARGET_TOOL = {TARGET_TOOL or "unknown"}
- QUERY_TYPE = {QUERY_TYPE}

Research typically takes 2-8 minutes (niche topics take longer). Starting now.
```

---

## Research Execution

### Step 1: Run the Research Script (FOREGROUND)

**CRITICAL: Run this in the FOREGROUND with a 5-minute timeout. Do NOT use run_in_background. The full output contains Reddit, X, AND YouTube data that you need to read completely.**

```bash
SKILL_ROOT=""
for dir in \
  ".claude/skills/last30days" \
  "${CLAUDE_PLUGIN_ROOT:-}" \
  "$HOME/.claude/skills/last30days"; do
  [ -n "$dir" ] && [ -f "$dir/scripts/last30days.py" ] && SKILL_ROOT="$dir" && break
done

if [ -z "${SKILL_ROOT:-}" ]; then
  echo "ERROR: Could not find scripts/last30days.py" >&2
  exit 1
fi

uv run python3 "${SKILL_ROOT}/scripts/last30days.py" "$ARGUMENTS" --emit=compact
```

Use a **timeout of 300000** (5 minutes) on the Bash call. The script typically takes 1-3 minutes.

The script will automatically:
- Detect available API keys from `~/.config/cherri/.env`
- Run Reddit search (via OpenAI Responses API + web_search)
- Run X search (via xAI Responses API + x_search)
- Run YouTube search (via yt-dlp)
- Output ALL results including YouTube transcripts

**Read the ENTIRE output.** It contains THREE data sections: Reddit items, X items, and YouTube items. If you miss the YouTube section, you will produce incomplete stats.

**YouTube items look like:** `**{video_id}** (score:N) {channel_name} [N views, N likes]` followed by a title, URL, and optional transcript snippet.

### API Key Setup

Keys are stored in `~/.config/cherri/.env`. Both are optional — the script degrades gracefully:

| Key | Source | Powers |
|-----|--------|--------|
| `OPENAI_API_KEY` | OpenAI | Reddit search (via web_search tool) |
| `XAI_API_KEY` | xAI (x.ai) | X/Twitter search (via x_search tool) |

YouTube search uses `yt-dlp` (no API key needed, must be installed via Homebrew).

**Modes based on available keys:**
- **Both keys**: Full Reddit + X + YouTube + WebSearch
- **One key**: Reddit-only or X-only + YouTube + WebSearch
- **No keys**: WebSearch + Exa fallback only

If keys are missing, add them to the shared Cherri config:
```bash
# Add to ~/.config/cherri/.env (shared with other Cherri tools)
OPENAI_API_KEY=sk-...
XAI_API_KEY=xai-...
```

**Options** (passed through from user's command):
- `--days=N` → Look back N days instead of 30
- `--quick` → Faster, fewer sources (8-12 each)
- (default) → Balanced (20-30 each)
- `--deep` → Comprehensive (50-70 Reddit, 40-60 X)

### Step 2: Supplement with WebSearch

After the script finishes, do WebSearch to supplement with blogs, tutorials, and news.

Choose search queries based on QUERY_TYPE:

**If RECOMMENDATIONS**: `best {TOPIC} recommendations`, `{TOPIC} list examples`, `most popular {TOPIC}`
**If NEWS**: `{TOPIC} news 2026`, `{TOPIC} announcement update`
**If PROMPTING**: `{TOPIC} prompts examples 2026`, `{TOPIC} techniques tips`
**If GENERAL**: `{TOPIC} 2026`, `{TOPIC} discussion`

Rules:
- **USE THE USER'S EXACT TERMINOLOGY** - don't substitute tech names based on your knowledge
- EXCLUDE reddit.com, x.com, twitter.com (covered by script)
- INCLUDE: blogs, tutorials, docs, news, GitHub repos
- **DO NOT output "Sources:" list** - save stats for the end

### Step 3: Exa Fallback (if script returned no results)

If the script found no API keys or returned errors, use Exa (`mcp__exa__web_search_exa`, load via ToolSearch) as fallback:

- `{TOPIC} site:reddit.com` (Reddit)
- `{TOPIC} site:x.com` (X/Twitter)
- `{TOPIC} site:youtube.com` (YouTube)
- Broad web search excluding the above domains

Filter to last 30 days using Exa's date filtering.

---

## Synthesis: Judge Agent

After all searches complete, internally synthesize:

1. Weight Reddit/X sources HIGHER (they have engagement signals: upvotes, likes)
2. Weight YouTube sources HIGH (views, likes, transcript content)
3. Weight WebSearch sources LOWER (no engagement data)
4. Identify patterns across ALL sources (strongest signals)
5. Note contradictions between sources
6. Extract top 3-5 actionable insights

**CRITICAL: Ground synthesis in ACTUAL research content, not pre-existing knowledge.**

- Use exact product/tool names from the research
- Cite specific insights from sources
- If research mentions "ClawdBot", don't conflate it with "Claude Code"

### If QUERY_TYPE = RECOMMENDATIONS

Extract SPECIFIC NAMES, not generic patterns:
- Scan research for specific product names, tool names, project names
- Count mentions across sources
- List by popularity/mention count

### For all QUERY_TYPEs

Identify from the ACTUAL RESEARCH OUTPUT:
- **PROMPT FORMAT** - Does research recommend JSON, structured, natural language, keywords?
- Top 3-5 patterns/techniques across multiple sources
- Specific keywords, structures, or approaches mentioned BY THE SOURCES
- Common pitfalls mentioned BY THE SOURCES

---

## Display Results

**FIRST - "What I learned" (based on QUERY_TYPE):**

**If RECOMMENDATIONS:**
```
Most mentioned:

[Tool Name] - {n}x mentions
Use Case: [what it does]
Sources: @handle1, @handle2, r/sub, blog.com

[Tool Name] - {n}x mentions
...

Notable mentions: [other specific things with 1-2 mentions]
```

CRITICAL for RECOMMENDATIONS: Each item MUST have a "Sources:" line with actual @handles, subreddit names, and web sources from the research.

**If PROMPTING/NEWS/GENERAL:**

CITATION RULES:
- Cite sparingly — 1 source per pattern, short format: "per @handle" or "per r/sub"
- Priority: @handles from X > r/subreddits > YouTube channels > web sources
- Never paste raw URLs — use publication names ("per Rolling Stone", not the URL)
- Lead with people, not publications
- Do NOT include engagement metrics in citations — save those for the stats box

```
What I learned:

**{Topic 1}** - [1-2 sentences about what people are saying, per @handle or r/sub]

**{Topic 2}** - [1-2 sentences, per @handle or r/sub]

KEY PATTERNS from the research:
1. [Pattern] - per @handle
2. [Pattern] - per r/sub
3. [Pattern] - per @handle
```

**THEN - Stats (right before invitation):**

Calculate actual totals from the research output. Parse `[Xlikes, Yrt]` from X posts, `[Xpts, Ycmt]` from Reddit.

```
---
All agents reported back!
├─ Reddit: {N} threads │ {N} upvotes │ {N} comments
├─ X: {N} posts │ {N} likes │ {N} reposts
├─ YouTube: {N} videos │ {N} views │ {N} with transcripts
├─ Web: {N} pages (supplementary)
└─ Top voices: @{handle1} ({N} likes), @{handle2} │ r/{sub1}, r/{sub2}
---
```

If a source returned 0, note it. If YouTube wasn't available, omit the line.

**LAST - Invitation (adapt to QUERY_TYPE):**

Every invitation MUST include 2-3 specific example suggestions based on what you ACTUALLY learned:

**If PROMPTING:**
```
I'm now an expert on {TOPIC} for {TARGET_TOOL}. What do you want to make? For example:
- [specific idea based on popular technique from research]
- [specific idea based on trending style/approach]
- [specific idea riffing on what people are creating]

Just describe your vision and I'll write a prompt you can paste straight into {TARGET_TOOL}.
```

**If RECOMMENDATIONS:**
```
I'm now an expert on {TOPIC}. Want me to go deeper? For example:
- [Compare specific item A vs item B from results]
- [Explain why item C is trending right now]
- [Help you get started with item D]
```

**If NEWS:**
```
I'm now an expert on {TOPIC}. Some things you could ask:
- [Follow-up about the biggest story]
- [Implications of a key development]
- [What might happen next]
```

**If GENERAL:**
```
I'm now an expert on {TOPIC}. Some things I can help with:
- [Question about the most discussed aspect]
- [Practical application of what you learned]
- [Deeper dive into a pattern or debate]
```

---

## WAIT FOR USER RESPONSE

After the stats and invitation, STOP and wait.

---

## When User Responds

- **Question** about the topic - answer from your research (no new searches)
- **Go deeper** on a subtopic - elaborate using research findings
- **Create something** - write ONE perfect prompt (see below)
- **Prompt** explicitly requested - write ONE perfect prompt

Only write a prompt when the user wants one. Don't force a prompt on someone who asked a question.

### Writing a Prompt

Match the FORMAT the research recommends:
- Research says JSON prompts - write JSON
- Research says structured parameters - use key: value format
- Research says natural language - use prose

```
Here's your prompt for {TARGET_TOOL}:

---

[The actual prompt IN THE FORMAT THE RESEARCH RECOMMENDS]

---

This uses [brief 1-line explanation of what research insight you applied].
```

Quality checklist:
- FORMAT MATCHES RESEARCH
- Directly addresses what the user wants to create
- Uses specific patterns/keywords from research
- Ready to paste with zero edits

---

## After Each Prompt: Stay in Expert Mode

```
---
Expert in: {TOPIC} for {TARGET_TOOL}
Based on: {n} Reddit threads ({sum} upvotes) + {n} X posts ({sum} likes) + {n} YouTube videos ({sum} views) + {n} web pages

Want another prompt? Just tell me what you're creating next.
```

---

## Context Memory

For the rest of the conversation, remember:
- **TOPIC**: {topic}
- **TARGET_TOOL**: {tool}
- **KEY PATTERNS**: {top 3-5 patterns}
- **RESEARCH FINDINGS**: Key facts and insights

After research is complete, you are an EXPERT on this topic. Do NOT run new searches unless the user asks about a DIFFERENT topic. Answer follow-ups from what you already learned.
