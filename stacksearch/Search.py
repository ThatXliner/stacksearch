#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Bryan hu .

@Bryan hu .

Made with love by Bryan hu .

The primitive functions to use. # API
"""
import requests
from bs4 import BeautifulSoup as bs
from typing import Any
import httpx


def Search(
    Query: str,
    print_prog: bool = True,
    search_on_site: str = "stackoverflow",
    *args: Any,
    **kwargs: Any,
) -> dict:
    """This is the official API for the stacksearch module.

    Parameters
    ----------
    Query : str
        This is the query to search the stackexchange website for.
    print_prog : bool
        If True, prints the progress. Otherwise, it does not print the progress (the default is True).
    search_on_site : str
        The stackexchange website to search on (the default is "stackoverflow").
    *args : Any
        For backwards compatibility.
    **kwargs : Any
        For backwards compatibility.

    Returns
    -------
    dict
        In the format: {
        'question': ['answer1', 'answer2', ...], 'question2': ['answer1', ...]
        }

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
    r.raise_for_status()
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


async def fSearch(
    Query: str,
    print_prog: bool = True,
    search_on_site: str = "stackoverflow",
    *args: Any,
    **kwargs: Any,
) -> dict:
    """This is a in-development asynchronous version of the stable Search API. Should be faster.

    Parameters
    ----------
    Query : str
        This is the query to search the stackexchange website for.
    print_prog : bool
        If True, prints the progress. Otherwise, it does not print the progress (the default is True).
    search_on_site : str
        The stackexchange website to search on (the default is "stackoverflow").
    *args : Any
        For backwards compatibility.
    **kwargs : Any
        For backwards compatibility.

    Returns
    -------
    dict
        In the format: {
        'question': ['answer1', 'answer2', ...], 'question2': ['answer1', ...]
        }

    """

    async def _remove_dot_com(string: str) -> str:
        string = str(string)
        # Maybe a regex is better here...
        if string.endswith(".com"):
            return string[0 : len(string) - 4]
        elif string.endswith(".org"):
            return string[0 : len(string) - 4]
        else:
            return string

    async def ParsePages(links_for_pages):
        return (  # Pages of all the questions related to Query
            bs(link.content, "lxml") for link in links_for_pages
        )

    async def findAnswers(pages):
        return (
            (
                answer.find(attrs=TEXT_REQUIREMENTS).get_text()
                for answer in page.find_all(
                    attrs={"itemtype": "http://schema.org/Answer"}
                )
            )
            for page in pages
        )

    async def findQuestions(soup):
        return {  # The raw ingredients
            question.string: question.get("href")
            for question in soup.find_all(
                attrs={"class": "question-hyperlink", "data-gps-track": None}
            )
        }

    search_on_site = await _remove_dot_com(search_on_site)
    TEXT_REQUIREMENTS = {"class": "post-text", "itemprop": "text"}
    if print_prog:
        print(f"Requesting results from {search_on_site}...")
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://{search_on_site}.com/search?q={Query}"
        )  # NOTE: For python3.9, use the str.remove_suffix()
    r.raise_for_status()
    if print_prog:
        print("Parsing response HTML...")
    soup = bs(r.content, "lxml")
    if print_prog:
        print("Collecting question links...")
    questions = await findQuestions(soup)
    if print_prog:
        print("Requesting questions found (This may take a while)...")
    async with httpx.AsyncClient() as client:
        _links_for_pages = (
            await client.get(link)
            for link in map(
                lambda x: f"https://{search_on_site}.com" + x, iter(questions.values())
            )
        )
    if print_prog:
        print("Parsing questions found (This may take a while)...")
    pages = await ParsePages(_links_for_pages)
    if print_prog:
        print("Identifying question text...")
    full_questions = (page.find(attrs=TEXT_REQUIREMENTS).get_text() for page in pages)
    if print_prog:
        print("Identifying answers...")
    answers = await findAnswers(pages)
    return dict(zip(full_questions, answers))
