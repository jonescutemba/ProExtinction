---
name: edit-content
description: Change text, headings, links, pictures or SEO descriptions on the Pro Extinction website. Use for any edit to what visitors read.
---

# Change website content

1. **Find the source.** Text lives in `content/<lang>/<slug>.json`, a JSON list with one entry per line (heading, paragraph, list item).
   The local slug differs per language. `SITE` in `tools/build.py` maps each language's slugs to the English slug (`EN_OF`, `OF_EN`).
   - Menu labels and fixed interface text: `SITE` (labels) and `T` in `tools/build.py`.
   - Page descriptions for search engines: `content/seo/<lang>.json` (key = local slug, 120 to 160 characters).
   - Picture descriptions: `content/alt/<lang>.json` (key = picture number from `content/images.json`).
   - Privacy policy: `content/legal/<lang>.json`.
   - Diagram labels: `content/diagrams/<lang>.txt`.
   Never edit `site/`. It is regenerated.
2. **Check whether the page is original or AI.** In `SITE`, the last field is the address of the old language site (original text) or `None` (AI translation of English).
   - Editing English: list which AI translations have the same line and update them too (skill `translate`), or say clearly in the pull request that they are now behind.
   - Editing an original page in another language: only that file. Line numbers there do not match English.
   - Adding or removing a line in English shifts all AI translations of that page. Do the same in every AI translation, in the same place, in the same commit.
3. **Keep the structure.** Headings and picture positions are set by hand (`KINDS_BY_HAND`, `content/images.json` `where`). If a change moves lines, check those indexes still point to the right lines.
4. **Follow AGENTS.md:** no "I"-form rewrites (except cosmic extinction), no removed pages, open questions in `KORREKTUREN-OFFEN.md` stay open.
5. **Build and check:** `python tools/build_all.py`, then `python tools/check.py` must say "all good".
6. **Look at it:** `python tools/serve.py`, open the changed page in light and dark (`?theme=light`) and on a narrow window. For screenshots hide images (`img{visibility:hidden}`).
7. **Commit** sources and `site/` together, on a branch, then open a pull request with the template.
