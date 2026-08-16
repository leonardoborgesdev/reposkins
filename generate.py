#!/usr/bin/env python3
"""RepoSkins Master Kit - standalone generator.

Runs 100% locally. Never calls reposkins.pro or any hosted backend -
only the public GitHub API (api.github.com), with YOUR OWN token.
Writes SVGs to assets/ and a ready-to-paste README.md for your
special <username>/<username> profile repo.

Usage:
    export GITHUB_TOKEN=$(gh auth token)   # or a classic PAT, "repo" scope
    python generate.py YOUR_USERNAME --theme midnight
    python generate.py YOUR_USERNAME --theme github-dark --cards hero,wordmark,heatmap
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "generators"))

from github_api import get_user_data  # noqa: E402
from generators import hero, wordmark, heatmap, portrait, chess, system_scan, highlights, social_row, avatar, snake_trail  # noqa: E402
from badges import build_badges  # noqa: E402
import json  # noqa: E402

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "themes", "palettes.json"), encoding="utf-8") as _f:
    _PALETTES = json.load(_f)

FREE_THEMES = ("midnight", "github-dark")
ALL_CARDS = ("hero", "wordmark", "heatmap", "portrait", "chess", "system-scan", "highlights", "social-row", "avatar")
# Bonus card: a real GitSkins template, but only extracted in "midnight" - not
# part of the 8-card free promise, request it explicitly with --cards snake-trail
BONUS_CARDS = ("snake-trail",)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


def build_card(card, username, data, theme_name, heatmap_style, highlights_items, social_links):
    if card == "hero":
        return hero.render(username, data, theme_name)
    if card == "wordmark":
        return wordmark.render(username, data, theme_name)
    if card == "heatmap":
        return heatmap.render(username, data, theme_name, style=heatmap_style)
    if card == "portrait":
        return portrait.render(username, data, theme_name)
    if card == "chess":
        return chess.render(username, data, theme_name)
    if card == "system-scan":
        return system_scan.render(username, data, theme_name)
    if card == "highlights":
        return highlights.render(username, data, theme_name, items_raw=highlights_items)
    if card == "social-row":
        return social_row.render(username, data, theme_name, links_raw=social_links)
    if card == "snake-trail":
        if theme_name != "midnight":
            print(f"  NOTE: snake-trail only has a real 'midnight' template - rendering in midnight regardless of --theme {theme_name}")
        return snake_trail.render(username, data, theme_name)
    raise ValueError(f"unknown card: {card}")


def main():
    p = argparse.ArgumentParser(description="Generate RepoSkins cards locally, with no dependency on any external backend.")
    p.add_argument("username", help="your GitHub username")
    p.add_argument("--theme", default="midnight", choices=FREE_THEMES,
                   help=f"theme (the free kit only ships {FREE_THEMES}; the other 19 are at reposkins.pro)")
    p.add_argument("--cards", default="hero,wordmark,heatmap,portrait,chess,system-scan,highlights,social-row",
                   help="comma-separated list, from: " + ",".join(ALL_CARDS))
    p.add_argument("--heatmap-style", default="default", choices=("default", "jet", "snake", "erased"))
    p.add_argument("--highlights-items", default="Open source::Building in public::Shipping weekly")
    p.add_argument("--social-links", default="")
    p.add_argument("--include-avatar", action="store_true", help="also generate assets/avatar.png (procedural avatar, not your real GitHub photo)")
    p.add_argument("--badges", default="", help="e.g. linkedin:https://...,instagram:https://...,email:foo@bar.com (shields.io, no API call)")
    args = p.parse_args()

    if not os.environ.get("GITHUB_TOKEN"):
        print("WARNING: no GITHUB_TOKEN in the environment. Public data still works, but the")
        print("heatmap card comes back empty (the contributions query needs a token) and you'll")
        print("hit GitHub's 60 req/hour public rate limit fast. Recommended: export GITHUB_TOKEN=$(gh auth token)")
        print()

    cards = [c.strip() for c in args.cards.split(",") if c.strip()]
    os.makedirs(ASSETS_DIR, exist_ok=True)

    print(f"Fetching @{args.username}'s data directly from api.github.com...")
    data = get_user_data(args.username)

    generated = []
    for card in cards:
        print(f"  generating {card}.svg ({args.theme})...")
        svg = build_card(card, args.username, data, args.theme, args.heatmap_style, args.highlights_items, args.social_links)
        out_path = os.path.join(ASSETS_DIR, f"{card}.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg)
        generated.append(card)

    if args.include_avatar:
        print("  generating avatar.png (procedural)...")
        png_bytes = avatar.render_png(args.username)
        with open(os.path.join(ASSETS_DIR, "avatar.png"), "wb") as f:
            f.write(png_bytes)

    readme_lines = [
        f"<!-- generated locally by the RepoSkins Master Kit, theme {args.theme} -->",
        "",
    ]
    for card in generated:
        url = f"https://raw.githubusercontent.com/{args.username}/{args.username}/main/assets/{card}.svg"
        readme_lines.append(f"![{card}]({url})")
        readme_lines.append("")

    if args.badges:
        bg = _PALETTES[args.theme]["bg"][0]
        badges_html = build_badges(args.badges, bg)
        if badges_html:
            readme_lines += ["<p>" + badges_html + "</p>", ""]

    readme_path = os.path.join(BASE_DIR, "README.generated.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(readme_lines))

    print()
    print(f"Done. {len(generated)} SVGs in {ASSETS_DIR}")
    print(f"Markdown ready at {readme_path}")
    print()
    print("Next step (manual):")
    print(f"  1. Create the repo {args.username}/{args.username} through the GitHub web UI (check 'Add README')")
    print(f"  2. Copy the whole assets/ folder to that repo's root")
    print(f"  3. Copy README.generated.md's content into the repo's README.md")
    print(f"  Commit and push. Zero calls to any backend of ours from here on.")


if __name__ == "__main__":
    main()
