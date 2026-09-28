# Load the ~2760-skill catalog

Read this first. Do not dump thousands of skill names into the prompt.

Catalog: https://github.com/sickn33/agentic-awesome-skills (2476 SKILL.md playbooks, v18.8.0),
plus 284 extra skills from other reputable repos (anthropics/financial-services, Orchestra-Research/AI-Research-SKILLs,
huggingface/skills, mem0ai/mem0, vectorize-io/hindsight, paperclipai/paperclip, vercel-labs/json-render, ...). 2760 index entries in total.
They are `disable-model-invocation: true` on purpose. Search, then Read one file.

## Why

If you put all ~2760 descriptions into the system prompt, the chat gets worse.
Working pattern: one auto-invoked router + on-disk / Drive / GitHub catalog.

1. Search `skills_index.json` (Drive or this repo) or the installed skill folders.
2. Read only the winning `SKILL.md` (use the entry's `raw_url`).
3. Follow that playbook.

## grok.com

There is no bulk install into the Skills menu.

One-time: Settings → Customize → Custom Instructions → paste `grok/CUSTOM_INSTRUCTIONS.txt`.
After that, do not wait for the user to say “按目录做”.
On specialized work (review, debug, paper, UI, git, deploy, “how do I…”):

- Open https://drive.google.com/drive/folders/14oLXTT0B_wyzH4en5yjLOUEjpOerqgxJ
- Read HOW_TO_LOAD.md
- Search skills_index.json for the task
- Open only the winning entry's `raw_url`. Regular entries: https://raw.githubusercontent.com/sickn33/agentic-awesome-skills/main/<path>/SKILL.md
  Extra entries (`"external": true`) live in other repos; use their `raw_url` as-is.
- If no match, do the task directly
- Skip offensive / pentest skills unless the user asked

Optional: Skill Creator, one skill named `use-installed-skills`, same text as Custom Instructions.

## Cursor

Copy `use-installed-skills/` to `~/.cursor/skills/use-installed-skills/`.
Copy `rules/use-installed-skills.mdc` to `<repo>/.cursor/rules/`.
Clone the catalog separately; do not paste it into chat.

## Grok CLI / Grok Build

Copy `use-installed-skills/` to `~/.grok/skills/use-installed-skills/`.
Discovery is by SKILL.md `description`, not by stuffing ~2760 files.

## Do not

- Paste the catalog into the chat
- Ask the user to @ a skill unless they named one
- Load all ~2760 SKILL.md files at once
