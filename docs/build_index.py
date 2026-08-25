#!/usr/bin/env python3
"""
Build the browsable index for the 2110101 COMP PROG site.

Scans the repository for problem folders (<topic>/<code>/) and writes
docs/assets/data.js, a single JS file the site loads with a <script> tag
(no fetch, so the page also works when opened straight from disk).

Usage:  python3 docs/build_index.py
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "assets", "data.js")

# Content larger than this is not embedded in full.
EMBED_LIMIT = 32_000
PREVIEW = 4_000

SKIP_DIRS = {"docs", "Work-Shop", ".git", "__pycache__"}
TOPIC_RE = re.compile(r"^(\d{2}|P\d)-(.+)$")


def topic_label(folder):
    m = TOPIC_RE.match(folder)
    if not m:
        return folder.replace("-", " ")
    return m.group(2).replace("-", " ")


def topic_key(folder):
    m = TOPIC_RE.match(folder)
    return m.group(1) if m else folder


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def pack(path):
    """Embed a text file, trimming very large ones to a preview."""
    size = os.path.getsize(path)
    text = read_text(path)
    if len(text) <= EMBED_LIMIT:
        return {"size": size, "text": text}
    return {"size": size, "text": text[:PREVIEW], "trunc": True}


def title_of(problem_dir, code):
    """Problem title, taken from the header comment of the solution."""
    py = os.path.join(problem_dir, code + ".py")
    if os.path.exists(py):
        for line in read_text(py).splitlines()[:10]:
            m = re.match(r"^#\s*\S+\s*:\s*(.+)$", line.strip())
            if m:
                return m.group(1).strip()
    readme = os.path.join(problem_dir, "README.md")
    if os.path.exists(readme):
        for line in read_text(readme).splitlines()[:5]:
            m = re.match(r"^#\s*\S+\s*:\s*(.+)$", line.strip())
            if m:
                return m.group(1).strip()
    return code


def collect_sets(problem_dir, rel):
    sets = {}
    for name in ("examplesets", "testsets"):
        in_dir = os.path.join(problem_dir, "testcases", name, "input")
        out_dir = os.path.join(problem_dir, "testcases", name, "output")
        if not os.path.isdir(in_dir):
            continue
        cases = []
        for fn in sorted(os.listdir(in_dir)):
            m = re.match(r"^input(\d+)\.txt$", fn)
            if not m:
                continue
            n = int(m.group(1))
            out_fn = f"output{m.group(1)}.txt"
            out_path = os.path.join(out_dir, out_fn)
            case = {
                "n": n,
                "in": pack(os.path.join(in_dir, fn)),
                "out": pack(out_path) if os.path.exists(out_path) else None,
                "inPath": f"{rel}/testcases/{name}/input/{fn}",
                "outPath": f"{rel}/testcases/{name}/output/{out_fn}",
            }
            cases.append(case)
        if cases:
            sets[name] = cases
    return sets


def main():
    topics = []
    problems = []

    for folder in sorted(os.listdir(ROOT)):
        full = os.path.join(ROOT, folder)
        if not os.path.isdir(full) or folder in SKIP_DIRS or folder.startswith((".", "_")):
            continue
        codes = sorted(
            d for d in os.listdir(full)
            if os.path.isdir(os.path.join(full, d)) and not d.startswith(".")
        )
        if not codes:
            continue
        topics.append({
            "id": folder,
            "key": topic_key(folder),
            "label": topic_label(folder),
            "count": len(codes),
        })
        for code in codes:
            pdir = os.path.join(full, code)
            rel = f"{folder}/{code}"
            files = os.listdir(pdir)

            data_files = []
            ddir = os.path.join(pdir, "data")
            if os.path.isdir(ddir):
                for fn in sorted(os.listdir(ddir)):
                    if fn.startswith("."):
                        continue
                    d = pack(os.path.join(ddir, fn))
                    d["name"] = fn
                    d["path"] = f"{rel}/data/{fn}"
                    data_files.append(d)

            sets = collect_sets(pdir, rel)
            entry = {
                "code": code,
                "title": title_of(pdir, code),
                "topic": folder,
                "dir": rel,
                "pdf": f"{rel}/{code}.pdf" if f"{code}.pdf" in files else None,
                "py": f"{rel}/{code}.py" if f"{code}.py" in files else None,
                "source": read_text(os.path.join(pdir, code + ".py")) if f"{code}.py" in files else None,
                "data": data_files,
                "sets": sets,
                "nExample": len(sets.get("examplesets", [])),
                "nTest": len(sets.get("testsets", [])),
            }
            problems.append(entry)

    payload = {"topics": topics, "problems": problems}
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("// Generated by docs/build_index.py - do not edit by hand.\n")
        f.write("window.CP_DATA = ")
        f.write(body)
        f.write(";\n")

    cases = sum(p["nExample"] + p["nTest"] for p in problems)
    print(f"topics   : {len(topics)}")
    print(f"problems : {len(problems)}")
    print(f"cases    : {cases}")
    print(f"written  : {OUT} ({os.path.getsize(OUT):,} bytes)")


if __name__ == "__main__":
    sys.exit(main())
