#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Bryan hu .

@Bryan hu .

Made with love by Bryan hu .

The primitive functions to use.
"""
import requests
from bs4 import BeautifulSoup as bs
from typing import Any


def Search(
    Query: str,
    print_prog: bool = True,
    search_on_site: str = "stackoverflow",
    # Including the "stackexchange.com" (if present) but not the ".com" suffix
    *args: Any,
    **kwargs: Any,
) -> dict:
    """For getting very precise information on StackOverflow. This is the function you should use.

    Returns
    -------
    dict
        A dict containing the raw data of the questions/answers gotten.

    """

    def _remove_dot_com(string: str) -> str:
        string = str(string)
        # Maybe a regex is better here...
        if string.endswith(".com"):
            return string[0 : len(string) - 4]
        elif string.endswith(".org"):
            return string[0 : len(string) - 4]
        else:
            return string

    search_on_site = _remove_dot_com(search_on_site)
    TEXT_REQUIREMENTS = {"class": "post-text", "itemprop": "text"}
    if print_prog:
        print(f"Requesting results from {search_on_site}...")
    r = requests.get(
        f"https://{search_on_site}.com/search?q={Query}"
    )  # NOTE: For python3.9, use the str.remove_suffix()
    if print_prog:
        print("Parsing response HTML...")
    soup = bs(r.content, "lxml")
    if print_prog:
        print("Collecting question links...")
    questions = {  # The raw ingredients
        question.string: question.get("href")
        for question in soup.find_all(
            attrs={"class": "question-hyperlink", "data-gps-track": None}
        )
    }
    if print_prog:
        print("Requesting questions found (This may take a while)...")
    _links_for_pages = (
        requests.get(link)
        for link in map(
            lambda x: f"https://{search_on_site}.com" + x, iter(questions.values())
        )
    )
    if print_prog:
        print("Parsing questions found (This may take a while)...")
    pages = [  # Pages of all the questions related to Query
        bs(link.content, "lxml") for link in _links_for_pages
    ]
    if print_prog:
        print("Identifying question text...")
    full_questions = [page.find(attrs=TEXT_REQUIREMENTS).get_text() for page in pages]
    if print_prog:
        print("Identifying answers...")
    answers = [
        [
            answer.find(attrs=TEXT_REQUIREMENTS).get_text()
            for answer in page.find_all(attrs={"itemtype": "http://schema.org/Answer"})
        ]
        for page in pages
    ]
    return dict(zip(full_questions, answers))
