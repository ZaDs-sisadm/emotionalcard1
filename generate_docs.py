"""
generate_docs.py
================

Documentation generator for the EmotionalCards project.

Reads docstrings from all modules in ``components/`` and ``cookie_popup/``
using Python's built-in :mod:`inspect` and :mod:`ast` modules, then writes
a combined HTML documentation file to ``docs/index.html``.

Alternatively you can use **pdoc** for richer output::

    pip install pdoc
    pdoc --html --output-dir docs components/ cookie_popup/

Run this script directly::

    python generate_docs.py
"""

import ast
import os
import sys
import textwrap
import datetime


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODULES = [
    ("components/card.py",            "Card",            "Basic Component"),
    ("components/emotional_card.py",  "EmotionalCard",   "Complex Component"),
    ("cookie_popup/gdpr_cookie.py",   "GDPRCookieConsent", "GDPR Module"),
]

OUTPUT_PATH = "docs/generated.html"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_docstrings(filepath: str) -> dict:
    """Parse a Python source file and extract module + class + function docstrings.

    Args:
        filepath (str): Path to the ``.py`` source file.

    Returns:
        dict: A mapping with keys ``"module"``, ``"classes"``, ``"functions"``.
    """
    with open(filepath, encoding="utf-8") as fh:
        source = fh.read()

    tree = ast.parse(source)
    result: dict = {"module": "", "classes": [], "functions": []}

    # Module docstring
    result["module"] = ast.get_docstring(tree) or ""

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node) or "(no docstring)"
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    mdoc = ast.get_docstring(item) or ""
                    args = [a.arg for a in item.args.args if a.arg != "self"]
                    methods.append({"name": item.name, "doc": mdoc, "args": args})
            result["classes"].append({
                "name": node.name,
                "doc": doc,
                "methods": methods,
            })

        elif isinstance(node, ast.FunctionDef) and not any(
            isinstance(parent, ast.ClassDef)
            for parent in ast.walk(tree)
            if hasattr(parent, "body") and node in getattr(parent, "body", [])
        ):
            doc = ast.get_docstring(node) or ""
            args = [a.arg for a in node.args.args if a.arg not in ("self", "cls")]
            result["functions"].append({"name": node.name, "doc": doc, "args": args})

    return result


def html_escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_module_html(filepath: str, label: str, badge: str) -> str:
    """Render HTML documentation for a single module.

    Args:
        filepath (str): Path to the source file.
        label    (str): Human-readable module name.
        badge    (str): Badge text shown next to the heading.

    Returns:
        str: HTML string for the module section.
    """
    data = extract_docstrings(filepath)
    filename = os.path.basename(filepath)

    parts = [
        f'<section>',
        f'<h2>{label} <span class="badge">{badge}</span></h2>',
        f'<p><em>Source: <code>{filepath}</code></em></p>',
    ]

    if data["module"]:
        synopsis = data["module"].split("\n")[0]
        parts.append(f"<p>{html_escape(synopsis)}</p>")

    for cls in data["classes"]:
        parts += [
            f'<div class="card">',
            f'<h3>class <code>{cls["name"]}</code></h3>',
            f'<p>{html_escape(cls["doc"].split(chr(10))[0])}</p>',
        ]
        if cls["methods"]:
            parts.append("<table><thead><tr><th>Method</th><th>Args</th><th>Description</th></tr></thead><tbody>")
            for m in cls["methods"]:
                mdoc_short = html_escape(m["doc"].split("\n")[0]) if m["doc"] else "—"
                args_str   = ", ".join(m["args"]) or "—"
                parts.append(
                    f'<tr><td><code>{m["name"]}</code></td>'
                    f'<td><code>{html_escape(args_str)}</code></td>'
                    f'<td>{mdoc_short}</td></tr>'
                )
            parts.append("</tbody></table>")
        parts.append("</div>")

    parts.append("</section>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Generate HTML documentation to ``docs/generated.html``."""
    os.makedirs("docs", exist_ok=True)

    body_parts = []
    for filepath, label, badge in MODULES:
        if os.path.exists(filepath):
            body_parts.append(render_module_html(filepath, label, badge))
        else:
            print(f"[WARNING] File not found: {filepath}", file=sys.stderr)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>EmotionalCards — Generated Docs</title>
<style>
  body {{font-family:'Segoe UI',sans-serif;max-width:900px;margin:40px auto;padding:0 24px;color:#222;}}
  h1 {{color:#1e1e2e;}}
  h2 {{border-bottom:2px solid #4f9cf9;padding-bottom:6px;margin-top:40px;}}
  h3 {{color:#333;margin-top:20px;}}
  code {{background:#f0f4f8;padding:2px 6px;border-radius:4px;font-size:.9em;}}
  pre  {{background:#1e1e2e;color:#cdd6f4;padding:16px;border-radius:8px;overflow-x:auto;}}
  .card {{border:1px solid #e0e0e0;border-radius:10px;padding:20px;margin:16px 0;}}
  .badge {{background:#dbeafe;color:#1d4ed8;padding:2px 10px;border-radius:20px;font-size:.8em;font-weight:600;}}
  table {{width:100%;border-collapse:collapse;margin:12px 0;}}
  th,td {{text-align:left;padding:8px 12px;border-bottom:1px solid #eee;}}
  th {{background:#f8f9fa;}}
  p {{line-height:1.7;}}
</style>
</head>
<body>
<h1>📖 EmotionalCards — API Documentation</h1>
<p>Auto-generated by <code>generate_docs.py</code> on {now}</p>
<hr/>
{"".join(body_parts)}
<footer style="margin-top:48px;padding-top:16px;border-top:1px solid #eee;
               color:#999;font-size:.85em;text-align:center;">
  EmotionalCards · КОП Lab 1 · MIT License
</footer>
</body>
</html>"""

    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(html)

    print(f"✅ Documentation written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
