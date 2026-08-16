# Master Prompt — RepoSkins Free Kit

Cards · contribution snake · social badges. One prompt, four phases.

**Read this first.** This generates real cards from your real GitHub data,
running entirely on your machine. It never calls reposkins.pro or any shared
backend — only `api.github.com` (with your own token), `img.shields.io`
(badge images), and GitHub's own Actions runners for the snake. Free tier is
2 themes (`midnight`, `github-dark`) across 8 card types; the other 19 themes
and 4 remaining card types live in the hosted paid version if you'd rather
not run anything locally.

**You need:** Python 3.10+, the [`gh` CLI](https://cli.github.com) (or a
classic GitHub PAT, `repo` scope), and a GitHub account. Budget 10–15 minutes.

---

## ▼ THE PROMPT — copy everything from here to "END OF PROMPT" ▼

I want to set up my animated GitHub profile using the RepoSkins Master Kit in
this repository. Walk me through it step by step, and check in with me after
each phase before moving to the next.

**My details**
- GitHub username: `[USERNAME]` (profile repo will be `[USERNAME]/[USERNAME]`, branch `main`)
- Theme: `midnight` or `github-dark` — I choose: `[THEME]`
- Cards I want: `[e.g. hero,wordmark,heatmap,portrait,chess,system-scan,highlights,social-row]`
- My social links for badges (optional): `[e.g. linkedin:https://..., instagram:https://..., email:me@example.com]`

### PHASE 1 — Authenticate

Run `gh auth status`. If I'm not logged in, walk me through `gh auth login`.
Then export the token: `export GITHUB_TOKEN=$(gh auth token)`. Without this,
the heatmap card comes back empty (the contribution-calendar query needs a
token) and I'll hit the public API's 60-requests/hour limit fast.

### PHASE 2 — Generate

Run:
```
python generate.py [USERNAME] --theme [THEME] --cards [CARDS] --with-snake --badges "[BADGES]"
```
This writes `assets/*.svg`, a ready `README.generated.md`, and tells me which
`github-actions/snake-[THEME].yml` to use. Show me the generated SVGs (open
them, don't just say it worked) before we move on.

### PHASE 3 — The special repo

Remind me the repo must be named exactly `[USERNAME]/[USERNAME]` and must be
created through GitHub's **web UI**, not the API or `gh repo create` — with
"Add a README file" checked. A repo created via API sometimes fails to
trigger GitHub's special profile display. This is the step people skip and
then ask me why nothing shows up.

### PHASE 4 — Publish

Help me: copy `assets/` into the cloned profile repo's root, copy
`github-actions/snake-[THEME].yml` to `.github/workflows/snake.yml`, copy
`README.generated.md`'s contents into `README.md`, `git add`, `git commit`,
`git push`.

Then, for the snake specifically: remind me to set **Settings → Actions →
General → Workflow permissions → Read and write** on the repository (not my
account settings), and to run the workflow once manually before expecting
the snake to show up — the `output` branch doesn't exist until that first run
finishes green.

### If something "didn't change"

Check the file first: open the raw URL with a cache-busting
`?v=999` query string, or view-source. It's almost always GitHub's CDN cache,
not a generator bug. Also confirm I'm looking at the theme I actually chose —
dark and light snake assets only render in their matching color scheme.

Tell me when I'm wrong — if a step won't work the way I described it, say so
instead of trying it anyway.

## ▲ END OF PROMPT ▲

---

## What to expect

| Phase | Effort | Iteration? |
|---|---|---|
| 1 — Authenticate | 2 min | No |
| 2 — Generate | 3 min | Maybe — re-run with different `--cards` or `--theme` |
| 3 — Special repo | 2 min | No, but easy to get wrong once |
| 4 — Publish + snake | 5–10 min | No — the only wait is the first Action run |

Phases 2–4 are copy-paste and could be done without any AI assistant at
all — the prompt exists so you get one continuous session instead of
switching between this document and a terminal.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Heatmap card is empty | No `GITHUB_TOKEN` set | `export GITHUB_TOKEN=$(gh auth token)` before running |
| `rate limit exceeded` | Unauthenticated public API, 60 req/hour | Same fix as above |
| Special profile view never shows up | Repo created wrong | Recreate via the **web UI**, exact name `username/username`, README checked |
| Image doesn't update on the profile | GitHub's camo cache | Append `?v=2`, `?v=3`... to the image URL in the README |
| Snake image 404s | `output` branch doesn't exist yet | Run the Action once manually (Actions → Run workflow) and wait for green |
| LinkedIn badge shows text but no icon | shields.io only renders the LinkedIn logo on brand color `#0A66C2` | Already handled in `badges.py` — LinkedIn is always forced to brand color regardless of theme |
| Action fails with a permissions error on push | Workflow permissions default to read-only | Settings → Actions → General → Workflow permissions → **Read and write**, on the repo, not the account |

## What's not in the free kit, and why

`about`, `stats`, and `stack` cards are excluded on purpose — right now they
only render pixel-perfect in the `midnight` theme even in the hosted product,
and shipping a mis-themed card for free felt worse than not shipping it. The
other 19 themes require a real per-theme template, extracted by hand; that
work is what funds the hosted version at reposkins.pro.
