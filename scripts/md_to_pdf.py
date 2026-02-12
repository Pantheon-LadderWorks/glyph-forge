#!/usr/bin/env python3
"""
Markdown to PDF converter using WeasyPrint.
Full Unicode/emoji support, no LaTeX drama.
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path
import sys

# CSS for beautiful PDF rendering
STYLE = """
@page {
    size: letter;
    margin: 1in;
}

body {
    font-family: 'Segoe UI', 'Noto Sans', sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
}

h1 {
    font-size: 18pt;
    border-bottom: 2px solid #333;
    padding-bottom: 0.3em;
    margin-top: 1.5em;
}

h2 {
    font-size: 14pt;
    color: #2c3e50;
    margin-top: 1.5em;
    border-bottom: 1px solid #ccc;
    padding-bottom: 0.2em;
}

h3 {
    font-size: 12pt;
    color: #34495e;
}

code {
    font-family: 'Cascadia Mono', 'Consolas', 'Courier New', monospace;
    background-color: #f4f4f4;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 10pt;
}

pre {
    font-family: 'Cascadia Mono', 'Consolas', 'Courier New', monospace;
    background-color: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 1em;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.4;
}

pre code {
    background: none;
    padding: 0;
}

blockquote {
    border-left: 4px solid #7c3aed;
    margin-left: 0;
    padding-left: 1em;
    color: #555;
    font-style: italic;
}

strong {
    color: #1a1a1a;
}

em {
    color: #444;
}

hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 2em 0;
}

ul, ol {
    margin-left: 1.5em;
}

li {
    margin-bottom: 0.3em;
}

/* Math-like styling for inline LaTeX-ish content */
.math {
    font-family: 'Cambria Math', 'STIX Two Math', serif;
    font-style: italic;
}
"""

def md_to_pdf(input_path: str, output_path: str = None):
    """Convert markdown file to PDF."""
    input_file = Path(input_path)
    
    if output_path is None:
        output_path = input_file.with_suffix('.pdf')
    else:
        output_path = Path(output_path)
    
    # Read markdown
    md_content = input_file.read_text(encoding='utf-8')
    
    # Convert to HTML with extensions
    html_content = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'tables', 'nl2br']
    )
    
    # Wrap in full HTML document
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{input_file.stem}</title>
</head>
<body>
{html_content}
</body>
</html>
"""
    
    # Generate PDF
    html_doc = HTML(string=full_html)
    css = CSS(string=STYLE)
    html_doc.write_pdf(output_path, stylesheets=[css])
    
    print(f"✅ PDF generated: {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python md_to_pdf.py <input.md> [output.pdf]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    md_to_pdf(input_file, output_file)
