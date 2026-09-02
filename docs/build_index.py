#!/usr/bin/env python3
"""
Build the browsable index for the 2110101 COMP PROG site.

Scans the repository for problem folders (<topic>/<code>/) and writes
docs/assets/data.js, a single JS file the site loads with a <script> tag
(no fetch, so the page also works when opened straight from disk).

Usage:  python3 docs/build_index.py
"""

import json
import io
import keyword
import os
import re
import sys
import tokenize
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "assets", "data.js")

# Content larger than this is not embedded in full.
EMBED_LIMIT = 32_000
PREVIEW = 4_000

SKIP_DIRS = {"docs", "Work-Shop", ".git", "__pycache__"}
TOPIC_RE = re.compile(r"^(\d{2}|P\d)-(.+)$")
IMAGE_EXTENSIONS = {".gif", ".jpeg", ".jpg", ".png", ".webp"}
AUDIO_EXTENSIONS = {".mp3", ".ogg", ".wav"}
VIDEO_EXTENSIONS = {".mp4", ".webm"}
PY_BUILTINS = {
    "abs", "all", "any", "bin", "bool", "chr", "dict", "divmod", "enumerate", "eval", "exec",
    "filter", "float", "format", "frozenset", "getattr", "hex", "input", "int", "isinstance", "iter",
    "len", "list", "map", "max", "min", "next", "object", "oct", "open", "ord", "pow", "print",
    "range", "repr", "reversed", "round", "set", "setattr", "slice", "sorted", "str", "sum", "super",
    "tuple", "type", "zip", "self",
}


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


def notebook_source(value):
    """Return a notebook source field as text (it may be a list or string)."""
    return "".join(value) if isinstance(value, list) else str(value or "")


def highlight_python(source):
    """Return escaped Python source with the site's token classes applied."""
    starts = [0]
    for match in re.finditer("\n", source):
        starts.append(match.end())

    def offset(position):
        line, column = position
        return starts[line - 1] + column if line - 1 < len(starts) else len(source)

    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        out = []
        cursor = 0
        for token in tokens:
            start = offset(token.start)
            end = offset(token.end)
            out.append(escape(source[cursor:start]))
            value = source[start:end]
            css_class = None
            if token.type == tokenize.COMMENT:
                css_class = "tok-com"
            elif token.type == tokenize.STRING:
                css_class = "tok-str"
            elif token.type == tokenize.NUMBER:
                css_class = "tok-num"
            elif token.type == tokenize.NAME:
                if keyword.iskeyword(value):
                    css_class = "tok-kw"
                elif value in PY_BUILTINS:
                    css_class = "tok-bi"
            escaped = escape(value)
            out.append(f'<span class="{css_class}">{escaped}</span>' if css_class else escaped)
            cursor = end
        out.append(escape(source[cursor:]))
        return "".join(out)
    except (tokenize.TokenError, IndentationError):
        return escape(source)


def notebook_code_html(source):
    """Render one notebook code cell using the same editor affordances as the site."""
    lines = source.rstrip("\n").split("\n") if source else [""]
    gutter = "\n".join(str(number) for number in range(1, len(lines) + 1))
    return (f'<div class="code-wrap"><pre class="gutter" aria-hidden="true">{gutter}</pre>'
            f'<pre class="code"><code>{highlight_python(source)}</code></pre></div>')


def render_notebook_html(notebook, title):
    """Render a dependency-free, readable HTML view of a Jupyter notebook."""
    parts = [
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">",
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
        f"<title>{escape(title)}</title>",
        "<style>body{max-width:980px;margin:0 auto;padding:32px;font:16px/1.6 system-ui,sans-serif;color:#292522;background:#faf9f8}h1{line-height:1.2}section{margin:24px 0}.markdown{white-space:pre-wrap}.code-wrap{display:flex;overflow:hidden;border-radius:8px;background:#272822}.code,pre{overflow:auto;padding:16px;border-radius:8px;background:#272822;color:#f8f8f2;font:13px/1.6 ui-monospace,SFMono-Regular,Consolas,monospace}.gutter{margin:0;padding:16px 12px 16px 16px;flex:none;text-align:right;color:#8b9284;border-radius:0;border-right:1px solid #3b3c35;user-select:none}.code{margin:0;flex:1;min-width:0;border-radius:0}.output{background:#fff;border:1px solid #e5e0dc;color:#292522}.tok-kw{color:#cf94e8;font-weight:500}.tok-str{color:#96d1a0}.tok-num{color:#efa971}.tok-com{color:#8d9585;font-style:italic}.tok-bi{color:#bda4ef}img{max-width:100%;height:auto}</style></head><body>",
        f"<h1>{escape(title)}</h1>",
    ]
    for cell in notebook.get("cells", []):
        cell_type = cell.get("cell_type")
        source = notebook_source(cell.get("source"))
        if cell_type == "markdown":
            parts.append(f"<section class=\"markdown\">{escape(source)}</section>")
        elif cell_type == "code":
            parts.append(f"<section>{notebook_code_html(source)}")
            for output in cell.get("outputs", []):
                output_type = output.get("output_type")
                if output_type == "stream":
                    parts.append(f"<pre class=\"output\">{escape(notebook_source(output.get('text')))}</pre>")
                    continue
                if output_type == "error":
                    parts.append(f"<pre class=\"output\">{escape(notebook_source(output.get('traceback')))}</pre>")
                    continue
                data = output.get("data", {})
                if "image/png" in data:
                    parts.append(f"<img alt=\"Notebook output\" src=\"data:image/png;base64,{data['image/png']}\">")
                elif "text/html" in data:
                    parts.append(f"<div class=\"output\">{notebook_source(data['text/html'])}</div>")
                elif "text/plain" in data:
                    parts.append(f"<pre class=\"output\">{escape(notebook_source(data['text/plain']))}</pre>")
            parts.append("</section>")
    parts.append("</body></html>")
    return "".join(parts)


def workshop_resource(path, rel_path, name):
    """Describe a workshop file in the form needed by the resource viewer."""
    ext = os.path.splitext(name)[1].lower()
    item = {"name": name, "path": rel_path, "size": os.path.getsize(path)}
    if ext == ".py":
        item["kind"] = "code"
        item.update(pack(path))
    elif ext in IMAGE_EXTENSIONS:
        item["kind"] = "image"
    elif ext in AUDIO_EXTENSIONS:
        item["kind"] = "audio"
    elif ext in VIDEO_EXTENSIONS:
        item["kind"] = "video"
    else:
        item["kind"] = "file"
    return item


def collect_workshops(root, docs_dir):
    """Index workshop folders and export each notebook to a static HTML reader."""
    base = os.path.join(root, "Work-Shop")
    if not os.path.isdir(base):
        return []
    workshops = []
    for folder in sorted(os.listdir(base)):
        workshop_dir = os.path.join(base, folder)
        if not os.path.isdir(workshop_dir) or folder.startswith("."):
            continue
        rel = f"Work-Shop/{folder}"
        slides = []
        notebooks = []
        resources = []
        for current, dirs, files in os.walk(workshop_dir):
            dirs[:] = sorted(d for d in dirs if not d.startswith("."))
            for fn in sorted(f for f in files if not f.startswith(".")):
                path = os.path.join(current, fn)
                relative_name = os.path.relpath(path, workshop_dir)
                relative_path = f"{rel}/{relative_name}"
                if fn.lower().endswith(".pdf"):
                    slides.append({"name": relative_name, "path": relative_path})
                elif fn.lower().endswith(".ipynb"):
                    html_rel = f"generated/workshops/{folder}/{os.path.splitext(fn)[0]}.html"
                    html_path = os.path.join(docs_dir, html_rel)
                    with open(path, encoding="utf-8") as f:
                        notebook = json.load(f)
                    os.makedirs(os.path.dirname(html_path), exist_ok=True)
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(render_notebook_html(notebook, os.path.splitext(fn)[0]))
                    notebooks.append({"name": relative_name, "path": relative_path, "html": html_rel})
                else:
                    resources.append(workshop_resource(path, relative_path, relative_name))
        workshops.append({"id": folder, "title": folder.replace("-", " "), "slides": slides,
                          "notebooks": notebooks, "resources": resources})
    return workshops


def main():
    topics = []
    problems = []
    workshops = collect_workshops(ROOT, HERE)

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

    payload = {"topics": topics, "problems": problems, "workshops": workshops}
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
    print(f"workshops: {len(workshops)}")
    print(f"written  : {OUT} ({os.path.getsize(OUT):,} bytes)")


if __name__ == "__main__":
    sys.exit(main())
