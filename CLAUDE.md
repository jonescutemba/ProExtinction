@AGENTS.md

## Claude Code
- `.claude/settings.json` adds a guard hook (`.claude/hooks/guard.py`) that blocks the protected photos, hand edits of generated files, secret files, force pushes and pushes to `main`. If it blocks you, follow its message. Do not work around it.
- Skills in `.claude/skills/`: `edit-content` (change text), `translate` (add or update AI translations), `review` (check a pull request before an owner merges it).
- Before you finish a task: `python tools/check.py` must say "all good". Report what you changed and anything you skipped.
