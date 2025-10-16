# add_collapsible_headings.py — README

Purpose
- Post-process an exported Jupyter HTML file and add accessible collapsible headings that group markdown headings with their following code cells/outputs.
- Adds keyboard support (Enter/Space), ARIA attributes, and a small Expand all / Collapse all toolbar.

Quick usage (Windows PowerShell)

1) Export notebook to HTML using nbconvert (from repo root)

```powershell
jupyter nbconvert --to html "shear_moment_diagram.ipynb"
```

2) Run the post-processor (input -> output)

```powershell
python c:\workspace\github.com\concrete_calcs\data\add_collapsible_headings.py \
  "c:\workspace\github.com\concrete_calcs\data\shear_moment_diagram.html" \
  "c:\workspace\github.com\concrete_calcs\shear_moment_diagram_collapsible.html"
```

Optional: start sections collapsed

```powershell
python c:\workspace\github.com\concrete_calcs\data\add_collapsible_headings.py input.html output.html --collapse-by-default
```

Files
- Script: `c:\workspace\github.com\concrete_calcs\data\add_collapsible_headings.py`
- Example generated output: `c:\workspace\github.com\concrete_calcs\shear_moment_diagram_collapsible.html`

What it injects
- A small CSS block for the toggle and wrapper styles.
- Inline JavaScript that:
  - Finds headings (`h1..h6`), locates their enclosing notebook cell, and wraps the following `.jp-Cell` siblings until the next heading of the same/higher level.
  - Inserts a toggle button (a11y: `button`, `aria-expanded`, `aria-controls`) into each heading.
  - Adds keyboard handling (Enter/Space) for toggling.
  - Adds a global toolbar (Expand all / Collapse all) at the top of the page.

Accessibility notes
- Toggles are real `<button>` elements with `aria-expanded` and `aria-controls`.
- Headings are made focusable (`tabindex="0"`) and act as buttons for keyboard users.
- If needed, the wrappers can be enhanced with `role="region"` and `aria-labelledby` for extra screen-reader clarity.

Troubleshooting
- If toggles don’t appear:
  - Ensure nbconvert completed successfully and you passed the correct input HTML path.
  - The script injects JS that runs on DOMContentLoaded; if your HTML has unusual structure, open the file and check for the injected script near the end of `<body>`.

Optional improvements
- Sticky toolbar: add `position: sticky; top: 0; background: white; z-index: 999;` to the toolbar.
- Smooth transitions: replace `display` toggling with a CSS `max-height` transition and a collapsed class (requires measuring/setting max heights).

Contact / next steps
- If you want, I can add the sticky-toolbar CSS, smooth transitions, or add a short top-level README entry. Tell me which and I'll implement it.
