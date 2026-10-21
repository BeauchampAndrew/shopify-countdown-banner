"""Copies the CSS and JS from the section into demo/index.html.

Run after changing sections/countdown-banner.liquid:
    python3 demo/build_demo.py
"""
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
section = (root / "sections" / "countdown-banner.liquid").read_text()
demo_path = root / "demo" / "index.html"
demo = demo_path.read_text()


def block(tag):
    return re.search(r"{%\s*" + tag + r"\s*%}\n(.*?){%\s*end" + tag + r"\s*%}", section, re.S).group(1)


def fill(html, name, content):
    pattern = re.compile(r"(<!-- build:" + name + r" .*?-->\n)(.*?)(\s*<!-- /build:" + name + r" -->)", re.S)
    return pattern.sub(lambda m: m.group(1) + content + "\n    " + m.group(3).lstrip(), html, count=1)


demo = fill(demo, "css", "    <style>\n" + block("stylesheet") + "    </style>")
demo = fill(demo, "js", "    <script>\n" + block("javascript") + "    </script>")
demo_path.write_text(demo)
print("Updated", demo_path.relative_to(root))
