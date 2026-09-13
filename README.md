# skill-router-pack

One router + an index. Not 2121 skills dumped into a prompt.

- Catalog: [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills)
- Drive index folder: https://drive.google.com/drive/folders/14oLXTT0B_wyzH4en5yjLOUEjpOerqgxJ
- CI zip: GitHub → Actions → latest run artifacts / Releases

## CI ↔ Google Drive

On `main` push / manual dispatch, [`.github/workflows/release.yml`](.github/workflows/release.yml):

1. **Pulls** `skills_index.json` from Drive into the pack (when secrets are set)
2. Builds `dist/skill-router-pack.zip`
3. Creates a GitHub Release
4. **Uploads** the zip back to the same Drive folder

### Secrets (repo → Settings → Secrets and variables → Actions)

| Secret | Value |
|--------|--------|
| `GDRIVE_CREDENTIALS` | Full Google Cloud **service account** JSON (not an API key) |
| `GDRIVE_FOLDER_ID` | `14oLXTT0B_wyzH4en5yjLOUEjpOerqgxJ` (or your folder id) |

### One-time Google setup (service account + shared folder)

1. Google Cloud Console → enable **Google Drive API** (not “API key”)
2. Create a service account → add a **JSON** key → note `client_email`
3. Open the Drive folder → Share → paste `client_email` as **Editor** (turn off notify)
4. Put the JSON and folder id into the two GitHub Secrets above

Uploads **must** use the shared folder id. New service accounts have no personal Drive quota; without sharing + `--drive-root-folder-id`, uploads fail with 403.

If secrets are missing, CI still zips and releases; Drive steps are skipped.

## grok.com

Settings → Customize → Custom Instructions → paste [grok/CUSTOM_INSTRUCTIONS.txt](grok/CUSTOM_INSTRUCTIONS.txt). New chats only.
