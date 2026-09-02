# Problem browser

A static site for reading everything in this repository: problem statements,
solutions, and the full set of grader test cases.

## Running it

Open `docs/index.html` in a browser, or serve the repository root:

```bash
python3 -m http.server 8000
# then open http://localhost:8000/docs/
```

## Reading code comfortably

The solution view has a **Dark code / Light code** button. The page itself stays
light; only the code surface flips, because a bright white slab of small
monospace type is the part that tires the eye. The choice is remembered in
`localStorage`, so it survives a reload.

## Publishing on GitHub Pages

In **Settings → Pages**, set the source to the **`main` branch, `/ (root)` folder**.

The root — not `/docs` — because the site links out to the PDFs, test cases and
data files that live in the topic folders. Publishing only `/docs` would leave
those files unreachable and every statement would 404. `index.html` at the root
redirects to `docs/`, so the published URL stays clean, and `.nojekyll` keeps
GitHub from dropping the `_`-prefixed data files.

## Rebuilding the index

`assets/data.js` is generated. Re-run the build after adding or changing a problem or workshop:

```bash
python3 docs/build_index.py
```

The script walks every `<topic>/<code>/` folder and collects the statement path,
the solution source, each test case, and any data files. It also walks every
`Work-Shop/<name>/` folder: PDFs appear as slide decks, and each `.ipynb` is
exported to a static HTML reader under `docs/generated/workshops/`. Content over
32 KB is stored as a preview, with the site linking to the full file. Other
workshop assets are indexed recursively: Python files use the highlighted code
viewer, images appear in a gallery, and audio files have an inline player.

## Files

| File | Purpose |
|---|---|
| `index.html` | Page shell |
| `assets/style.css` | Styles |
| `assets/app.js` | Navigation, search, syntax highlighting |
| `assets/data.js` | Generated index — do not edit by hand |
| `build_index.py` | Regenerates `assets/data.js` |
