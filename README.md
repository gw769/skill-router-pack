# skill-router-pack

One router + an index. Not 2121 skills dumped into a prompt.

- Catalog: [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills)
- Drive index folder: https://drive.google.com/drive/folders/14oLXTT0B_wyzH4en5yjLOUEjpOerqgxJ
- CI zip: GitHub → Actions → latest run artifacts / Releases

## CI ↔ Google Drive

On `main` push / manual dispatch, [`.github/workflows/release.yml`](.github/workflows/release.yml):

1. **Pulls** `skills_index.json` from Drive into the pack (when secrets are set)
2. Builds `dist/skill-router-pack.zip`
3. **Updates** a specific, existing user-owned Drive ZIP
4. Creates a GitHub Release

This is a packaging pipeline, not a general two-way folder sync. Drive edits do
not trigger it. Only a main push or manual dispatch does.

### Secrets (repo → Settings → Secrets and variables → Actions)

| Secret | Value |
|--------|--------|
| `GDRIVE_CREDENTIALS` | Full Google Cloud **service account** JSON (not an API key) |
| `GDRIVE_FOLDER_ID` | `14oLXTT0B_wyzH4en5yjLOUEjpOerqgxJ` (or your folder id) |
| `GDRIVE_ZIP_FILE_ID` | ID of an existing user-owned ZIP that CI may update |

### One-time Google setup (service account + shared folder)

1. Google Cloud Console → enable **Google Drive API** (not “API key”)
2. Create a service account → add a **JSON** key → note `client_email`
3. Open the Drive folder → Share → paste `client_email` as **Editor** (turn off notify)
4. Using your own account, create the destination ZIP once and grant this service account access.
5. Put the JSON, source folder ID and destination ZIP file ID into the three secrets above.

The source folder ID is used for reading the index. The destination FILE ID is
used to update the ZIP. Sharing a My Drive folder does not give a service account
storage quota for new files; the existing user-owned file is essential here.

Credentials are step-scoped, stored in mode-0600 temporary files and removed by
an EXIT trap even on failure. They are not part of the ZIP or Release.

## Local Codex / Agents search

Copy `use-installed-skills` into your skill directory. Place the optional
`skills_index.json` from the Release beside its SKILL.md. Then run:

```bash
python3 ~/.codex/skills/use-installed-skills/scripts/search.py "论文 写作" --limit 5
```

Search reads local files only. It checks Codex, Agents, Cursor and Grok roots,
deduplicates resolved paths, and distinguishes installed from catalog-only entries.
Read the selected playbook fully before acting. Downloading an index is not
installing all catalog skills and does not grant authority to run their scripts.

If secrets are missing, CI still zips and releases; Drive steps are skipped.

## grok.com

Settings → Customize → Custom Instructions → paste [grok/CUSTOM_INSTRUCTIONS.txt](grok/CUSTOM_INSTRUCTIONS.txt). New chats only.
