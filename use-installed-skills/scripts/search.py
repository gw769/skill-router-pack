#!/usr/bin/env python3
"""Read-only search of installed Codex/Agents skills and optional catalog."""
import argparse
import json
import re
import subprocess
import shutil
from pathlib import Path
from urllib.parse import quote

BASE = Path(__file__).resolve().parents[1]
ALIASES = {"论文": "paper research", "写作": "writing", "引用": "citation",
           "调试": "debugging", "代码审查": "code review", "训练": "training",
           "测试": "testing", "部署": "deployment", "绘图": "plotting"}

def tokens(text):
    return set(re.findall(r"[a-z0-9]+", str(text).lower()))

def score(query, row):
    return 5 * len(query & tokens(row["name"])) + len(query & tokens(row["description"]))

def local_rows():
    roots = [str(Path.home() / p) for p in (".codex/skills", ".agents/skills", ".cursor/skills", ".grok/skills")
             if (Path.home() / p).is_dir()]
    if not roots:
        return []
    if shutil.which("rg"):
        result = subprocess.run(["rg", "--files", "--hidden", "-L", *roots, "-g", "SKILL.md"],
                                capture_output=True, text=True)
        if result.returncode not in (0, 1):
            raise RuntimeError("Could not inventory local skills")
        paths = result.stdout.splitlines()
    else:
        paths = [str(p) for root in roots for p in Path(root).rglob("SKILL.md")]
    rows, seen = [], set()
    for raw in paths:
        path = Path(raw).resolve()
        if path in seen:
            continue
        seen.add(path)
        text = path.read_text(encoding="utf-8", errors="replace")
        parts = text.split("---", 2)
        header = parts[1] if text.startswith("---") and len(parts) == 3 else ""
        name = re.search(r"(?m)^name:\s*(.+)$", header)
        rows.append(dict(name=name.group(1).strip().strip("\"'") if name else path.parent.name,
                         description=header, path=str(path), status="installed"))
    return rows

def catalog_rows(index):
    if not index.is_file():
        return []
    rows = []
    data = json.loads(index.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Index must be a list")
    for row in data:
        path = str(row.get("path", "")).strip("/")
        if not path or ".." in path.split("/") or ":" in path:
            continue
        if not path.endswith("SKILL.md"):
            path += "/SKILL.md"
        rows.append(dict(name=row.get("name") or row.get("id", ""),
                         description=str(row.get("description", "")), status="catalog-only",
                         path="https://github.com/sickn33/agentic-awesome-skills/blob/main/" + quote(path, safe="/")))
    return rows

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--index", type=Path, default=BASE / "skills_index.json")
    args = parser.parse_args()
    if not 1 <= args.limit <= 30:
        parser.error("--limit must be 1..30")
    query = args.query
    for source, target in ALIASES.items():
        query = query.replace(source, " " + target + " ")
    query = tokens(query)
    rows = local_rows()
    names = {r["name"].lower() for r in rows}
    rows += [r for r in catalog_rows(args.index) if r["name"].lower() not in names]
    hits = [r for r in rows if score(query, r)]
    hits.sort(key=lambda r: (-score(query, r), r["status"] != "installed", r["path"]))
    for row in hits[:args.limit]:
        print(json.dumps({k: row[k] for k in ("name", "status", "path")}, ensure_ascii=False))
    if not hits:
        print("NO_MATCH")

if __name__ == "__main__":
    main()
