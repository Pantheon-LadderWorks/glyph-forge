#!/usr/bin/env python3
"""
Markdown to HTML converter with beautiful styling.
Open in browser, Ctrl+P, Save as PDF. Full Unicode support.
"""

import markdown
from pathlib import Path
import sys
import webbrowser

# Beautiful CSS for PDF-ready rendering
STYLE = """
@page {
    size: letter;
    margin: 1in;
}

@media print {
    body {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
}

* {
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', 'Noto Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 8.5in;
    margin: 0 auto;
    padding: 1in;
    background: white;
}

h1 {
    font-size: 18pt;
    border-bottom: 2px solid #333;
    padding-bottom: 0.3em;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

h1:first-of-type {
    margin-top: 0;
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
    font-family: 'Cascadia Code', 'Cascadia Mono', 'Consolas', 'Courier New', monospace;
    background-color: #f4f4f4;
    padding: 0.15em 0.4em;
    border-radius: 3px;
    font-size: 10pt;
}

pre {
    font-family: 'Cascadia Code', 'Cascadia Mono', 'Consolas', 'Courier New', monospace;
    background-color: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 1em;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.5;
    white-space: pre-wrap;
    word-wrap: break-word;
}

pre code {
    background: none;
    padding: 0;
    font-size: inherit;
}

blockquote {
    border-left: 4px solid #7c3aed;
    margin-left: 0;
    margin-right: 0;
    padding-left: 1em;
    color: #555;
    font-style: italic;
}

strong {
    color: #1a1a1a;
    font-weight: 600;
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
    padding-left: 0;
}

li {
    margin-bottom: 0.3em;
}

p {
    margin: 0.8em 0;
}

/* Math rendering - make $...$ content look nice */
.math-inline {
    font-family: 'Cambria Math', 'STIX Two Math', 'Times New Roman', serif;
    font-style: italic;
}

/* Table styling */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}

th {
    background-color: #f4f4f4;
    font-weight: 600;
}

/* Header block styling */
.header-block {
    margin-bottom: 2em;
}

.header-block p {
    margin: 0.3em 0;
}
"""

def process_math(text):
    """Simple processing for LaTeX-style math to make it render nicely."""
    import re
    
    # Replace $$...$$ with styled divs (display math)
    def replace_display_math(match):
        content = match.group(1).strip()
        return f'<div style="text-align: center; font-family: \'Cambria Math\', serif; font-style: italic; margin: 1em 0; font-size: 12pt;">{content}</div>'
    
    text = re.sub(r'\$\$(.*?)\$\$', replace_display_math, text, flags=re.DOTALL)
    
    # Replace $...$ with styled spans (inline math)
    def replace_inline_math(match):
        content = match.group(1)
        return f'<span style="font-family: \'Cambria Math\', serif; font-style: italic;">{content}</span>'
    
    text = re.sub(r'\$([^$]+)\$', replace_inline_math, text)
    
    return text

def md_to_html(input_path: str, output_path: str = None, open_browser: bool = True):
    """Convert markdown file to styled HTML."""
    input_file = Path(input_path)
    
    if output_path is None:
        output_path = input_file.with_suffix('.html')
    else:
        output_path = Path(output_path)
    
    # Read markdown
    md_content = input_file.read_text(encoding='utf-8')
    
    # Process math before markdown conversion
    md_content = process_math(md_content)
    
    # Convert to HTML with extensions
    html_content = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'tables', 'nl2br']
    )
    
    # Wrap in full HTML document
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{input_file.stem}</title>
    <style>
{STYLE}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""
    
    # Write HTML
    output_path.write_text(full_html, encoding='utf-8')
    print(f"✅ HTML generated: {output_path}")
    
    if open_browser:
        webbrowser.open(output_path.as_uri())
        print("📄 Opened in browser. Press Ctrl+P to print/save as PDF.")
    
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python md_to_html.py <input.md> [output.html] [--no-open]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = None
    open_browser = True
    
    for arg in sys.argv[2:]:
        if arg == '--no-open':
            open_browser = False
        else:
            output_file = arg
    
    md_to_html(input_file, output_file, open_browser)
