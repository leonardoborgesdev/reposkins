"""GitHub data fetching (REST + GraphQL), with an in-memory cache.
Single data source for the whole kit - nothing here calls
gitskins.com or any third-party service."""
import os
import time
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

_CACHE = {}
CACHE_TTL = 600


def get_user_data(username):
    now = time.time()
    hit = _CACHE.get(username)
    if hit and now - hit["t"] < CACHE_TTL:
        return hit["data"]

    user = requests.get(f"https://api.github.com/users/{username}", headers=HEADERS, timeout=10).json()
    repos = requests.get(
        f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated",
        headers=HEADERS, timeout=10,
    ).json()
    if not isinstance(repos, list):
        repos = []

    lang_counts = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
    total_lang = sum(lang_counts.values()) or 1
    langs = [
        {"name": k, "pct": round(v / total_lang * 100)}
        for k, v in sorted(lang_counts.items(), key=lambda kv: kv[1], reverse=True)[:6]
    ]

    stars = sum(r.get("stargazers_count", 0) for r in repos)

    pinned = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:4]
    projects = [
        {
            "name": r.get("name"),
            "description": r.get("description") or "",
            "stars": r.get("stargazers_count", 0),
            "language": r.get("language") or "",
            "url": r.get("html_url"),
        }
        for r in pinned
    ]

    contrib_weeks, contrib_total = [], 0
    if GITHUB_TOKEN:
        query = """
        query($login: String!) {
          user(login: $login) {
            contributionsCollection {
              contributionCalendar {
                totalContributions
                weeks { contributionDays { contributionCount date } }
              }
            }
          }
        }"""
        try:
            r = requests.post(
                "https://api.github.com/graphql",
                json={"query": query, "variables": {"login": username}},
                headers=HEADERS, timeout=10,
            ).json()
            cal = r["data"]["user"]["contributionsCollection"]["contributionCalendar"]
            contrib_total = cal["totalContributions"]
            contrib_weeks = cal["weeks"]
        except Exception:
            pass

    data = {
        "user": user,
        "langs": langs,
        "stars": stars,
        "repos_count": user.get("public_repos", len(repos)),
        "followers": user.get("followers", 0),
        "contrib_total": contrib_total,
        "contrib_weeks": contrib_weeks,
        "projects": projects,
    }
    _CACHE[username] = {"t": now, "data": data}
    return data


def get_avatar_bytes(avatar_url):
    r = requests.get(avatar_url, timeout=10)
    return r.content
