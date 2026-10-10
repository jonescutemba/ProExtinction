---
name: translate
description: Add or update AI translations of Pro Extinction pages, SEO descriptions or alt texts in any of the 29 languages. Use when English changed or a translation is missing.
---

# Translate

English (`content/en/`) is the source. Only pages marked `None` in `SITE` (`tools/build.py`) are AI translations. Original texts in other languages are never replaced by translations.

## A page or changed lines
1. Find the pairs: for each language `l`, `OF_EN[l][<english-slug>]` is the local slug. Only translate where `SITE` marks the page as AI (`None`).
2. Translate line by line. The result has **exactly as many lines as the English file**, in the same order. Write it to a scratch text file, one line per entry.
3. Style (unslop): plain everyday words, active voice, short sentences, the way a native speaker would write it. No em dashes, straight quotes only, no flowery additions, nothing left out.
   Keep names, numbers, URLs, `Pro Extinction` and markup as in English. Headings stay headings. Right-to-left languages (ar, fa, ur) need no special characters.
4. Store it: `python tools/put_translation.py <lang> <local-slug> <english-slug> <textfile>`. It refuses wrong line counts, empty lines, em dashes and curly quotes.
5. For a few changed lines, edit those indexes in `content/<lang>/<slug>.json` directly instead, and keep the same style.

## SEO descriptions and alt texts
- `content/seo/<lang>.json`: key = local slug, 120 to 160 characters, says what the page offers, no keyword lists.
- `content/alt/<lang>.json`: the same keys as `en.json`. Translate the English description; never look at the pictures 8 to 21.

## Many languages at once
Split the languages into groups (for example de pl es it fr pt ru / nl uk tr id vi tl sw / zh ja ko th ar fa ur / hi bn mr te ta pa gu) and give each group to its own agent with these rules. Review the results before committing.

## Finish
`python tools/build_all.py` and `python tools/check.py` ("all good"), look at one translated page in the preview, then commit on a branch and open a pull request that lists the languages and pages, marked as AI translation.

## New language
This touches many tables in `tools/build.py` (`LANGS`, `FULL_AI`, `LANG_NAME`, `SITE`, `AI_MENU`, `T`, `VEIL`, `GIVE`, `TOP`, `FAQ_FIND`, `BORN`, `LEGAL_LABEL`, `HREFLANG` if needed) plus `content/seo`, `content/alt`, `content/diagrams` and possibly fonts. Ask an owner first. Search for an existing language code such as `'gu'` to find every place.
