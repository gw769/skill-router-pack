# Load the 2121-skill catalog

Read this first. Do not dump 2000 skill names into the prompt.

Catalog: https://github.com/sickn33/agentic-awesome-skills (~2121 SKILL.md playbooks).
They are `disable-model-invocation: true` on purpose. Search, then Read one file.

## Why

If you put all 2121 descriptions into the system prompt, the chat gets worse.
Working pattern: one auto-invoked router + on-disk / Drive / GitHub catalog.

1. Search `skills_index.json` (Drive) or the installed skill folders.
2. Read only the winning `SKILL.md`.
3. Follow that playbook.

## grok.com

There is no bulk install into the Skills menu.

One-time: Settings → Customize → Custom Instructions → paste `grok/CUSTOM_INSTRUCTIONS.txt`.
After that, do not wait for the user to say “按目录做”.
On specialized work (review, debug, paper, UI, git, deploy, “how do I…”):

- Open https://drive.google.com/drive/folders/14oLXTT0B_wyzH4en5yjLOUEjpOerqgxJ
- Read HOW_TO_LOAD.md
- Search skills_index.json for the task
- Open only https://raw.githubusercontent.com/sickn33/agentic-awesome-skills/main/<path>/SKILL.md
- If no match, do the task directly
- Skip offensive / pentest skills unless the user asked

Optional: Skill Creator, one skill named `use-installed-skills`, same text as Custom Instructions.

## Cursor

Copy `use-installed-skills/` to `~/.cursor/skills/use-installed-skills/`.
Copy `rules/use-installed-skills.mdc` to `<repo>/.cursor/rules/`.
Clone the catalog separately; do not paste it into chat.

## Codex

Copy `use-installed-skills/` to `~/.codex/skills/use-installed-skills/`.
Put the optional Release `skills_index.json` beside its `SKILL.md`.
Run `python3 ~/.codex/skills/use-installed-skills/scripts/search.py "paper writing" --limit 5`.
The script scans installed Codex, Agents, Cursor and Grok roots. It works without
an index and reports remote-only matches separately. No Cursor `.mdc` rule is
required for Codex; do not claim all catalog entries are installed.

## Grok CLI / Grok Build

Copy `use-installed-skills/` to `~/.grok/skills/use-installed-skills/`.
Discovery is by SKILL.md `description`, not by stuffing 2121 files.

## Do not

- Paste the catalog into the chat
- Ask the user to @ a skill unless they named one
- Load all 2121 SKILL.md files at once
