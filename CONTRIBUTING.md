# Contributing

Thank you for helping. You can change the website without being able to publish it: every change goes through a pull request, and one of the owners merges it. Only then does it go live.

## The short version
1. Get write access from an owner (or fork the repository).
2. Make a branch: `git switch -c your-name/what-you-change`.
3. Change the sources, never `site/` directly (see `AGENTS.md`).
4. Build and check: `python tools/build_all.py`, then `python tools/check.py`. It must end with "all good".
5. Look at your change: `python tools/serve.py`, then http://localhost:8000.
6. Commit the sources and the rebuilt `site/` together, push your branch, open a pull request and fill in the template.
7. The `check` job runs automatically. An owner reviews and merges. Within two minutes it is live.

You need Python 3.9 or newer and git. Nothing else to install.

## Working with AI
AI tools are welcome. `AGENTS.md` holds the rules every tool and person follows, and `CLAUDE.md` loads them into Claude Code automatically, together with a guard hook and three skills (`edit-content`, `translate`, `review`).
- Ask the AI to read `AGENTS.md` first if your tool does not do it by itself.
- You are responsible for what you submit. Read the diff before you open the pull request.
- Say in the pull request what the AI wrote or translated.
- Never give an AI tool tokens or passwords for this project. It needs none.

## What needs an owner's decision first
New pages or languages, design changes, anything that loads from other servers, stores data or adds a dependency, the switches `INDEXABLE` and `IMPRINT`, the privacy policy, the English core texts (manifesto, principles) and the open questions in `KORREKTUREN-OFFEN.md`. Open an issue or ask in the group before you start.
