"""Arctic Shift API client for subreddit-specific Reddit search.

Replaces the unauthenticated reddit.com/r/{sub}/search/.json endpoint
which returns 403. Arctic Shift is free, requires no API key, and
provides the same subreddit + keyword search capability.

Arctic Shift archives Reddit data with ~36-hour lag on engagement
scores and may lag weeks/months on indexing new posts. We use a
wider lookback (6 months) since Phase 2 supplemental search values
relevance over strict recency.

API docs: https://github.com/ArthurHeitmann/arctic_shift/tree/master/api
Base URL: https://arctic-shift.photon-reddit.com
"""

import re
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List
from urllib.parse import urlencode

from . import http

BASE_URL = "https://arctic-shift.photon-reddit.com"

# Common words that rarely help narrow a subreddit search
_STOPWORDS = frozenset(
    "a an the and or but not for in on about from with "
    "best top most popular latest recent new good great "
    "recommended favorite favourite what which how why "
    "should could would does are is do has have been "
    "women men womens mens people kids baby "
    "looking recommendations suggestions help advice".split()
)


def _log_info(msg: str):
    sys.stderr.write(f"[REDDIT] {msg}\n")
    sys.stderr.flush()


def search_subreddits(
    subreddits: List[str],
    topic: str,
    from_date: str,
    to_date: str,
    count_per: int = 5,
) -> List[Dict[str, Any]]:
    """Search specific subreddits via Arctic Shift API.

    Args:
        subreddits: List of subreddit names (without r/)
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        count_per: Results to request per subreddit

    Returns:
        List of item dicts matching the openai_reddit output format.
    """
    all_items = []
    seen_ids = set()
    keywords = _topic_to_keywords(topic)
    wide_after = _widen_lookback(from_date, months=6)

    for sub in subreddits:
        sub = sub.lstrip("r/")
        sub_posts = _search_one_subreddit(
            sub, keywords, wide_after, to_date, count_per,
        )

        for post in sub_posts:
            post_id = post.get("id", "")
            if post_id in seen_ids:
                continue
            seen_ids.add(post_id)

            permalink = post.get("permalink", "")
            if not permalink:
                permalink = f"/r/{sub}/comments/{post_id}/"

            item = {
                "id": f"RS{len(all_items)+1}",
                "title": str(post.get("title", "")).strip(),
                "url": f"https://www.reddit.com{permalink}",
                "subreddit": str(
                    post.get("subreddit", sub)
                ).strip(),
                "date": None,
                "why_relevant": (
                    f"Found in r/{sub} supplemental search"
                ),
                "relevance": 0.65,
            }

            created_utc = post.get("created_utc")
            if created_utc:
                from . import dates as dates_mod
                item["date"] = dates_mod.timestamp_to_date(
                    created_utc
                )

            all_items.append(item)

        _log_info(
            f"Arctic Shift r/{sub}: {len(sub_posts)} posts"
        )

    return all_items


def _search_one_subreddit(
    sub: str,
    keywords: List[str],
    after: str,
    before: str,
    limit: int,
) -> List[Dict[str, Any]]:
    """Search one subreddit, trying each keyword separately.

    Arctic Shift post title search is AND-only (no OR support),
    so we issue one request per keyword and merge unique posts.
    """
    seen = set()
    posts = []

    for kw in keywords:
        try:
            params = {
                "subreddit": sub,
                "title": kw,
                "after": after,
                "before": before,
                "limit": min(limit, 100),
                "sort": "desc",
            }
            url = f"{BASE_URL}/api/posts/search?{urlencode(params)}"
            data = http.get(url, timeout=15, retries=1)

            batch = data.get("data") or []
            for post in batch:
                if not isinstance(post, dict):
                    continue
                pid = post.get("id", "")
                if pid and pid not in seen:
                    seen.add(pid)
                    posts.append(post)

        except http.HTTPError as e:
            if e.status_code == 429:
                _log_info(
                    "Arctic Shift rate-limited — "
                    "skipping remaining keywords"
                )
                raise
            _log_info(
                f"Arctic Shift r/{sub} '{kw}': {e}"
            )
        except Exception as e:
            _log_info(
                f"Arctic Shift r/{sub} '{kw}' error: {e}"
            )

    return posts


def _widen_lookback(from_date: str, months: int = 6) -> str:
    """Push from_date back by N months for wider Arctic Shift coverage."""
    try:
        dt = datetime.strptime(from_date, "%Y-%m-%d")
        wider = dt - timedelta(days=months * 30)
        return wider.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return from_date


def _topic_to_keywords(topic: str) -> List[str]:
    """Extract distinctive keywords from a topic for search.

    Arctic Shift post title search is AND-only — all words must
    match. We extract the 2-3 most distinctive words and search
    for each separately, then merge results.
    """
    words = re.findall(r"[a-zA-Z]+", topic.lower())
    keywords = [w for w in words if w not in _STOPWORDS and len(w) > 2]

    if not keywords:
        return [topic]

    return keywords[:3]
