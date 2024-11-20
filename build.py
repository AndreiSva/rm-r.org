#!/usr/bin/env python3

import jinja2
import marko
import shutil
import datetime
import logging
import re
import sys

from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

output_path = Path("./build")
source_path = Path("./src")

def clean_build_directory():
    if output_path.exists() and output_path.is_dir():
        shutil.rmtree(output_path)
    elif output_path.exists() and not output_path.is_dir():
        logging.error("./build exists and is a file, quitting")
        sys.exit(1)
    output_path.mkdir(exist_ok=True)

def copy_static_files():
    for file_extension in ["*.css", "*.js", "*.ttf", "*.ico", "*.png", "*.jpg", "*.webp"]:
        for file_path in source_path.glob(file_extension):
            shutil.copy(file_path, output_path / file_path.name)

def load_template():
    with open(source_path / "template.html", "r") as f:
        return jinja2.Template(f.read())

def parse_metadata(content_text):
    meta = {}
    meta_pattern = re.compile(r"^META:\s*((?:.*\\\\\n\s*)*.*)")

    meta_match = meta_pattern.match(content_text)
    if meta_match:
        meta_text = meta_match.group(1)
        for entry in meta_text.split("\\"):
            if "=" in entry:
                metaname, metavalue = entry.split("=", 1)
                meta[metaname.strip()] = metavalue.strip()
    
    lines = content_text.split("\n")

    if meta_match is not None:
        content_text = "\n".join(lines[str(meta_match.group(1)).count("\n") + 1:])
    return meta, content_text

def convert_markdown_to_html(path, template):    
    with open(path, "r") as f:
        content_text = f.read()

    content_meta, content_text = parse_metadata(content_text)
    content_html = marko.convert(content_text)
    destdir = output_path / path.parent
    destdir.mkdir(parents=True, exist_ok=True)

    # Set up the default metadata
    page_meta = {
        "html_body": content_html,
        "html_year": datetime.date.today().year,
        "html_page": path.stem,

        # default to English
        "lang": "en"
    }

    with open(destdir / (path.stem + ".html"), "w") as f:
        page_meta.update(content_meta)
        f.write(template.render(page_meta))

def main():
    try:
        clean_build_directory()
        copy_static_files()
        template = load_template()

        for path in Path(".").rglob("*.md"):
            convert_markdown_to_html(path, template)
            
        logging.info("Done.")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()

