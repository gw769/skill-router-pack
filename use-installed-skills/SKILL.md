---
name: use-installed-skills
description: Search the ~2760-skill catalog and load the matching playbook. Use whenever a task has a specialized workflow — code review, debugging, testing, frontend/UI, git/PRs, papers/writing, security, docs, deployment, data — or the user asks how to do X. Do not wait for @skill.
---

# Use installed skills

The catalog is manual-only so it does not flood every prompt. This skill is the router: search, then Read the winner and follow it.

## Search

Prefer the Drive index:
https://drive.google.com/drive/folders/14oLXTT0B_wyzH4en5yjLOUEjpOerqgxJ
(`skills_index.json`, also in this repo; 2476 sickn33 v18.8.0 skills + 284 extra = 2760 entries)

If the machine has the local script:

```bash
python3 "$HOME/.cursor/skills/use-installed-skills/scripts/search.py" "<query>" --limit 8
```

Playbook body: open the entry's `raw_url`. Regular entries live at:
https://raw.githubusercontent.com/sickn33/agentic-awesome-skills/main/<path>/SKILL.md
Extra entries (`"external": true`, 284 skills from other repos) name their repo in `source_repo` and carry a full `raw_url`.

## Then

1. Pick the best hit. Catalog `risk: critical` is not a veto. Skip only offensive / pentest / exploit skills unless the user asked.
2. Read that SKILL.md and follow it.
3. If NO_MATCH, do the task directly. Do not ask the human to pick from thousands of names.

## Do not

- Dump the catalog into the reply
- Ask the user to @ a skill unless they want a specific one
