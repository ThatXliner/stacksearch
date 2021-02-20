#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate markdown from messy HTML"""

from typing import Optional, Union

from bs4 import BeautifulSoup, NavigableString


def reverse_markdown(html: BeautifulSoup) -> str:
    return generate_from_html(html.div)


def generate_from_html(html: Union[NavigableString, BeautifulSoup]) -> str:
    """The backend for `reverse_markdown`

    Specialized for StackExchange
    """
    if type(html) in (str, NavigableString):
        return html
    output = ""
    for child in html.children:
        if isinstance(child, NavigableString):
            output += child
        elif child.name == "p":
            output += generate_from_html(child)
        elif child.name == "pre":
            output += parse_code_block(child)
        elif child.name == "code":
            output += f"`{generate_from_html(child)}`"
        elif child.name == "hr":
            output += "\n---\n"
        elif child.name.startswith("h"):
            output += (
                "\n"
                + "#" * int(child.name[1:])
                + " "
                + generate_from_html(child)
                + "\n"
            )
        elif child.name in {"b", "strong"}:
            output += "**"
            for item in child.children:
                assert item is not None, "bold"
                output += generate_from_html(item)
            output += "**"
        elif child.name in {"i", "em"}:
            output += "*"
            for item in child.children:
                assert item is not None, "italic"
                output += generate_from_html(item)
            output += "*"
        elif child.name == "a":
            output += f"[{generate_from_html(child)}]({child['href']})"
        elif child.name == "img":
            output += f"![{child.get('alt')}]({child['src']})"
        elif child.name == "ul":
            for item in child("li"):
                output += f"\n * {generate_from_html(item)}"
        else:
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
    for item in ("default", "s-code-block", "hljs", "lang-sh"):
        try:
            classes.remove(item)
        except ValueError:
            pass
    if len(classes) == 0:
        return None
    assert len(classes) == 1, classes
    output = classes[0]
    if output.startswith("lang-"):
        output = output[5:]
    return output
