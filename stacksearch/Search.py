#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Bryan hu .

@Bryan hu .

Made with love by Bryan hu .

The primitive functions to use. # API
"""
import asyncio
import json
import random
import time
from pathlib import Path
from typing import Dict, List

import aiohttp
from bs4 import BeautifulSoup

TEXT_REQUIREMENTS = Path(__file__).parent.joinpath("txt_req.json").read_text()


def search(*args, **kwargs) -> Dict[str, List[str]]:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(fsearch(*args, **kwargs))


# from stacksearch import Search;Search.search("e")
async def fsearch(
    query: str,
    verbose: bool = False,
    search_on_site: str = "stackoverflow.com",
) -> Dict[str, List[str]]:
    """Use this. This is the async version of the Search API function.

    Parameters
    ----------
    query : str
        This is the query to search the stackexchange website for.
    verbose : bool
        If True, prints the progress. Otherwise, it does not print the progress
        (the default is False).
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

    async def find_questions(soup: BeautifulSoup) -> Dict[str, str]:
        return {
            question.string: question["href"]
            for question in soup.find_all(
                attrs={"class": "question-hyperlink", "data-gps-track": None}
            )
        }

    async def soupify(content: str) -> BeautifulSoup:
        return BeautifulSoup(content, features="html.parser")

    def get_answers_and_questions(page):
        try:
            stuff = page.find_all("div", attrs=json.loads(TEXT_REQUIREMENTS))
        except AttributeError as exception:
            raise RuntimeError(
                "Oh no! It appears that the StackOverflow's question text requirements "
                "have changed. Please go to the Git repository and submit a pull request "
                "to update the TEXT_REQUIREMENTS"
            ) from exception
        return stuff[0].get_text(), [answer.get_text() for answer in stuff[1:]]

    async with aiohttp.ClientSession() as client:
        ###
        # Get site
        ###
        if not search_on_site.endswith(".com") or not search_on_site.endswith(".org"):
            search_on_site = search_on_site + ".com"

        if verbose:
            print(f"Requesting results from {search_on_site}...")
        async with client.get(f"https://{search_on_site}/search?q={query}") as request:
            if request.status == 429:
                raise RuntimeError(
                    f"You have reached the maximum number of requests to {search_on_site}. Please try again later."
                )

            ###
            # Parse response
            ###
            if verbose:
                print("Parsing response HTML...")
            soup = await soupify(await request.text())
            if soup.find("div", class_="fs-body2 mb24"):
                raise RuntimeError("StackOverflow realized that we are not human")
            if verbose:
                print("Collecting question links...")
            question_links = await find_questions(soup)

            if verbose:
                print("Requesting questions found (This may take a while)...")
        question_html = []
        for link in map(
            lambda x: f"https://{search_on_site}{x}", iter(question_links.values())
        ):
            time.sleep(random.randint(1, 10) / 100)
            async with client.get(link) as request:
                question_html.append(await request.text())

        if verbose:
            print("Parsing questions found (This may take a while)...")
        pages = [await soupify(page) for page in question_html]

        if verbose:
            print("Returning results...")
        return dict(map(get_answers_and_questions, pages))
