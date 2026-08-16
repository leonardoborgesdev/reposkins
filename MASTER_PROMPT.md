# Master Prompt — RepoSkins Free Kit

Cards · Snake Trail · social badges. One prompt, three phases.

**Read this first.** This generates real cards from your real GitHub data,
running entirely on your machine. It never calls reposkins.pro or any shared
backend — only `api.github.com` (with your own token) and `img.shields.io`
(badge images). No GitHub Actions, no separate branch to wait on. Free tier
is 2 themes (`midnight`, `github-dark`) across 8 card types, plus a bonus
Snake Trail card that only has a real template in `midnight`. The other 19
themes and 3 remaining card types (`about`, `stats`, `stack`) live in the
hosted paid version if you'd rather not run anything locally.

**You need:** Python 3.10+, the [`gh` CLI](https://cli.github.com) (or a
classic GitHub PAT, `repo` scope), and a GitHub account. Budget 10 minutes.

---

## ▼ THE PROMPT — copy everything from here to "END OF PROMPT" ▼

I want to set up my animated GitHub profile using the RepoSkins Master Kit in
this repository. Walk me through it step by step, and check in with me after
each phase before moving to the next.

**My details**
- GitHub username: `[USERNAME]` (profile repo will be `[USERNAME]/[USERNAME]`, branch `main`)
- Theme: `midnight` or `github-dark` — I choose: `[THEME]`
- Cards I want: `[e.g. hero,wordmark,heatmap,portrait,chess,system-scan,highlights,social-row,snake-trail]`
- My social links for badges (optional): `[e.g. linkedin:https://..., instagram:https://..., email:me@example.com]`

### PHASE 1 — Authenticate and generate

Run `gh auth status`. If I'm not logged in, walk me through `gh auth login`.
Then export the token: `export GITHUB_TOKEN=$(gh auth token)`. Without this,
the heatmap and Snake Trail cards come back with an empty contribution
graph (the calendar query needs a token) and I'll hit the public API's
60-requests/hour limit fast.

Then run:
```
python generate.py [USERNAME] --theme [THEME] --cards [CARDS] --badges "[BADGES]"
```
This writes `assets/*.svg` and a ready `README.generated.md`. If `snake-trail`
is in my card list and my theme isn't `midnight`, tell me it rendered in
midnight colors anyway (that's expected — flag it, don't silently let it
pass). Show me the generated SVGs — open them, don't just say it worked —
before we move on.

### PHASE 2 — The special repo

Remind me the repo must be named exactly `[USERNAME]/[USERNAME]` and must be
created through GitHub's **web UI**, not the API or `gh repo create` — with
"Add a README file" checked. A repo created via API sometimes fails to
trigger GitHub's special profile display. This is the step people skip and
then ask me why nothing shows up.

### PHASE 3 — Publish

Help me: copy `assets/` into the cloned profile repo's root, copy
`README.generated.md`'s contents into `README.md`, `git add`, `git commit`,
`git push`. That's it — no Actions to enable, no branch to wait on, nothing
left running anywhere after this push.

### If something "didn't change"

Check the file first: open the raw URL with a cache-busting
`?v=999` query string, or view-source. It's almost always GitHub's CDN
cache, not a generator bug.

Tell me when I'm wrong — if a step won't work the way I described it, say so
instead of trying it anyway.

## ▲ END OF PROMPT ▲

---

## What to expect

| Phase | Effort | Iteration? |
|---|---|---|
| 1 — Authenticate + generate | 5 min | Maybe — re-run with different `--cards` or `--theme` |
| 2 — Special repo | 2 min | No, but easy to get wrong once |
| 3 — Publish | 2 min | No |

The whole thing is copy-paste and could be done without any AI assistant at
all — the prompt exists so you get one continuous session instead of
switching between this document and a terminal.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Heatmap or Snake Trail card is empty | No `GITHUB_TOKEN` set | `export GITHUB_TOKEN=$(gh auth token)` before running |
| `rate limit exceeded` | Unauthenticated public API, 60 req/hour | Same fix as above |
| Special profile view never shows up | Repo created wrong | Recreate via the **web UI**, exact name `username/username`, README checked |
| Image doesn't update on the profile | GitHub's camo cache | Append `?v=2`, `?v=3`... to the image URL in the README |
| Snake Trail looks like midnight even with `--theme github-dark` | Only a real `midnight` template exists for this card | Expected — request `--theme midnight` if you want it to match |
| LinkedIn badge shows text but no icon | shields.io only renders the LinkedIn logo on brand color `#0A66C2` | Already handled in `badges.py` — LinkedIn is always forced to brand color regardless of theme |

## What's not in the free kit, and why

`about`, `stats`, and `stack` cards are excluded on purpose — right now they
only render pixel-perfect in the `midnight` theme even in the hosted product,
and shipping a mis-themed card for free felt worse than not shipping it. The
other 19 themes require a real per-theme template, extracted by hand; that
work is what funds the hosted version at reposkins.pro.

An earlier version of this kit shipped a generic GitHub Actions contribution
snake (using [`Platane/snk`](https://github.com/Platane/snk)) instead of
Snake Trail. It worked, but looked nothing like the rest of the cards —
no card shell, no glow, a plain grid. Snake Trail replaces it entirely: same
visual language as every other card, and it's a static file instead of a
workflow that has to keep running.
