#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The main API for StackSearch"""
import asyncio
import json
import logging
import random
import time
from typing import Dict, List, Tuple

import aiohttp
from bs4 import BeautifulSoup

from . import reverse_markdown

TEXT_REQUIREMENTS: Dict[str, str] = {
    "class": "s-prose js-post-body",
    "itemprop": "text",
}
formatter = logging.Formatter("%(message)s")
handler = logging.NullHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.CRITICAL)

logger = logging.getLogger("stacksearch").addHandler(handler)


def sync_search(*args, **kwargs) -> Dict[str, List[str]]:
    """A synchronous version of search for synchronous code"""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(search(*args, **kwargs))


async def search(  # TODO: Use logger
    query: str,
    verbose: bool = False,
    search_on_site: str = "stackoverflow",
) -> Dict[str, List[str]]:  # TODO: Refactor
    """Use this. This is the async version of the Search API function.

    Parameters
    ----------
    query : str
        This is the query to search the StackExchange website for.
    verbose : bool
        If True, prints the progress. Otherwise, it does not print the progress
        (the default is False).
    search_on_site : str
        The StackExchange website to search on (the default is "stackoverflow").

    Returns
    -------
    dict
        In the format of

        .. code::

            {
                'question': ['answer1', 'answer2', ...], 'question2': ['answer1', ...]
            }

    """
    if verbose:
        logger.setLevel(logging.INFO)

    async def find_questions(soup: BeautifulSoup) -> Dict[str, str]:
        return {
            question.string: question["href"]
            for question in soup.find_all(
                attrs={"class": "question-hyperlink", "data-gps-track": None}
            )
        }

    async def soupify(content: str) -> BeautifulSoup:
        return BeautifulSoup(content, features="html.parser")

    def get_answers_and_questions(page: BeautifulSoup) -> Tuple[str, List[str]]:
        try:
            stuff = page("div", attrs=json.loads(TEXT_REQUIREMENTS))
        except AttributeError as exception:
            raise RuntimeError(
                "Oh no! It appears that the StackOverflow's question text requirements "
                "have changed. Please go to the Git repository and submit a pull request "
                "to update the TEXT_REQUIREMENTS"
            ) from exception
        return reverse_markdown.generate_from_html(stuff[0]), [
            reverse_markdown.generate_from_html(answer) for answer in stuff[1:]
        ]

    async with aiohttp.ClientSession() as client:
        ###
        # Get site
        ###
        if not (search_on_site.endswith(".com") or search_on_site.endswith(".org")):
            search_on_site += ".com"

        logger.info(f"Requesting results from {search_on_site}...")
        async with client.get(f"https://{search_on_site}/search?q={query}") as request:
            if request.status == 429:
                raise RuntimeError(
                    f"You have reached the maximum number of requests to {search_on_site}. Please try again later."
                )

            ###
            # Parse response
            ###
            logger.info("Parsing response HTML...")
            soup = await soupify(await request.text())
            if soup.find("div", class_="fs-body2 mb24"):  # Captcha test
                raise RuntimeError("StackOverflow realized that we are not human")
            logger.info("Collecting question links...")
            question_links = await find_questions(soup)

            logger.info("Requesting questions found (This may take a while)...")
        question_html = []
        for link in map(
            lambda x: f"https://{search_on_site}{x}", iter(question_links.values())
        ):
            time.sleep(random.randint(1, 10) / 100)
            async with client.get(link) as request:
                question_html.append(await request.text())

        logger.info("Parsing questions found (This may take a while)...")
        pages = [await soupify(page) for page in question_html]

        logger.info("Returning results...")
        return dict(map(get_answers_and_questions, pages))
