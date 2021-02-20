#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate markdown from messy HTML"""

from typing import Optional, Union

from bs4 import BeautifulSoup, NavigableString


def generate_from_html(html: Union[NavigableString, BeautifulSoup]) -> str:
    """The backend for :func:`stacksearch.search.reverse_html`

    Specialized for StackExchange
    """
    if type(html) in (str, NavigableString):
        return html
    output = ""
    for child in html.children:
        if isinstance(child, NavigableString):  # Strings
            output += child
        elif child.name == "div":  # Other text
            for item in child.children:
                output += generate_from_html(item)
        elif child.name == "p":  # Normal text
            output += generate_from_html(child)
        elif child.name == "pre":  # Code blocks
            output += parse_code_block(child)
        elif child.name == "code":  # Inline Code
            output += f"`{generate_from_html(child)}`"
        elif child.name == "hr":  # One of those line thingies
            output += "\n---\n"
        elif child.name.startswith("h"):  # Headers
            output += (
                "\n"
                + "#" * int(child.name[1:])
                + " "
                + generate_from_html(child)
                + "\n"
            )
        elif child.name in {"b", "strong"}:  # Bold
            output += "**"
            for item in child.children:
                assert item is not None, "bold"
                output += generate_from_html(item)
            output += "**"
        elif child.name in {"i", "em"}:  # Italics
            output += "*"
            for item in child.children:
                assert item is not None, "italic"
                output += generate_from_html(item)
            output += "*"
        elif child.name == "a":  # Link
            output += f"[{generate_from_html(child)}]({child['href']})"
        elif child.name == "img":  # Images
            output += f"![{child.get('alt')}]({child['src']})"
        elif child.name == "ul":  # Bullet list
            for item in child("li"):
                output += f"\n * {generate_from_html(item)}"
        elif child.name == "ol":  # Number list
            for index, item in enumerate(child("li")):
                output += f"\n{index + 1}. {generate_from_html(item)}"
        elif child.name == "br":
            output += "\n\n"
        else:  # Other HTML tags that weren't mentioned here
            output += str(child)

    return output


def parse_code_block(html: BeautifulSoup) -> str:
    output = ""
    output += f"\n```{detect_language(html) or ''}\n"
    output += html.code.get_text()
    output += "\n```\n"
    return output


def detect_language(html: BeautifulSoup) -> Optional[str]:
    classes = html.get("class")
    if classes is None:
        return None
    classes = classes[:]  # Copy it
    for item in (
        "default",
        "s-code-block",
        "hljs",
        "lang-sh",
        "snippet-code-js",
        "prettyprint-override",
    ):
        try:
            classes.remove(item)
        except ValueError:
            pass
    if len(classes) == 0:
        return None
    # assert len(classes) < 3, classes
    output = classes[-1]
    if output.startswith("lang-"):
        output = output[5:]
    if output.startswith("snippet-code-"):
        output = output[13:]
    return output
