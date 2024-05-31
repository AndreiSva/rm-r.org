#!/usr/bin/env python3

import jinja2
import marko
import shutil

from pathlib import Path

output_path = Path("./build")
source_path = Path("./src")

# clean the build directory and copy css and js files
if output_path.exists() and output_path.is_dir():
    shutil.rmtree(output_path)
output_path.mkdir(exist_ok=True)

# Copy all of the .js and .css files
for file_extension in ["*.css", "*.js"]:
    for file_path in source_path.glob(file_extension):
        shutil.copy(file_path, output_path / file_path.name)

# this is the base html template for all the pages
with open(source_path / "template.html", "r") as f:
    html_template_string = f.read()
html_template = jinja2.Template(html_template_string)

for path in Path(".").rglob("*.md"):
    with open(path, "r") as f:
        content_html = marko.convert(f.read())
    destdir = output_path / path.parent
    destdir.mkdir(parents=True, exist_ok=True)
    with open(destdir / (path.name.split(".")[0] + ".html"), "w") as f:
        data = {
            "html_body": content_html
        }
        f.write(html_template.render(data))
