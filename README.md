# skill-router-pack

One router + an index. Not 2121 skills dumped into a prompt.

- Catalog: [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills)
- Drive (same pack, anyone-with-link): https://drive.google.com/drive/folders/14oLXTT0B_wyzH4en5yjLOUEjpOerqgxJ

## grok.com (no extra phrase after one setup)

1. Open grok.com → Settings → Customize → Custom Instructions
2. Paste [grok/CUSTOM_INSTRUCTIONS.txt](grok/CUSTOM_INSTRUCTIONS.txt)
3. Save. New chats pick it up. Old chats do not.

## Cursor

Copy `use-installed-skills/` to `~/.cursor/skills/use-installed-skills/`.
Copy `rules/use-installed-skills.mdc` to the project `.cursor/rules/`.
Keep catalog skills `disable-model-invocation: true`.

## Grok CLI / Grok Build

Copy `use-installed-skills/` to `~/.grok/skills/use-installed-skills/`.
