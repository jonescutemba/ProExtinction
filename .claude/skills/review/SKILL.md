---
name: review
description: Review a Pro Extinction pull request or branch before an owner merges it. Checks safety, privacy, content rules and that the generated site matches its sources.
---

# Review a change

Compare the branch with `main` (`git diff main...HEAD`, or the pull request diff). Report findings ranked by severity, each with file and line, and a clear verdict: **merge**, **merge after fixes** or **do not merge**. Do not approve or merge yourself; an owner does that.

## Must hold (otherwise "do not merge")
1. `python tools/check.py --ci` passes on the branch (CI shows it as the `check` job).
2. **Nothing from other servers:** no new `http(s)://` in `<script>`, `<link>`, `<img>`, CSS `url()`, `fetch()` or `XMLHttpRequest`; the CSP in `hosting()` (`tools/build.py`) is not loosened.
3. **No tracking or data collection:** no new cookies, analytics, forms, embeds, or storage beyond settings. If there is any, the privacy policy (`content/legal/`) must change with it and an owner must have decided it.
4. **No secrets** and no new dependencies (Python stays standard library only; no `package.json` committed).
5. **Generated files match sources:** `site/` was not edited by hand (CI catches this).
6. **Switches unchanged** (`INDEXABLE`, `IMPRINT`, `SITE_URL`) unless the pull request says an owner asked for it.
7. **No unsafe HTML:** content inserted into pages goes through `esc()`; no `innerHTML` with text from the URL or storage; links opening a new tab have `rel="noopener"`.
8. **Workflow files** (`.github/`) and `.claude/` changes: no `pull_request_target`, no secrets in workflows, actions pinned to a commit SHA, permissions read-only. Owners review these line by line.

## Content
- English changes: are the AI translations of the same lines updated, or is the gap stated?
- AI translations: same line count as English, plain style, no em dashes or curly quotes, nothing added or left out (spot-check two or three lines per language by translating back).
- No page removed, no "I"-form rewritten (except cosmic extinction), no hand-set structure changed without a reason, no "original site" in AI notes.
- New pictures: WebP under 300 KB, alt texts in all languages. Never open the pictures 8 to 21.

## Look at it
Run `python tools/serve.py` and open the changed pages (desktop and narrow, light and dark, one right-to-left language if layout changed). Hide images in screenshots.
