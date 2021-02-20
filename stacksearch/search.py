#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The main API for StackSearch"""
import asyncio
import random
import time
from typing import Dict, List, Tuple

import aiohttp
from bs4 import BeautifulSoup

from . import errors, reverse_markdown

TEXT_REQUIREMENTS: Dict[str, str] = {
    "class": "s-prose js-post-body",
    "itemprop": "text",
}


def reverse_html(html: BeautifulSoup) -> str:
    """A more specialized version of :func:`stacksearch.reverse_markdown.generate_from_html`"""
    stackexchange_excuse = html.select(
        "div > aside > div > div > div.grid--cell.wmn0.fl1.lh-lg"
    )
    if stackexchange_excuse:
        info_text = stackexchange_excuse[0]
        html.div.aside.replace_with(info_text.contents[0])
    return reverse_markdown.generate_from_html(html).strip()


def sync_search(*args, **kwargs) -> Dict[str, List[str]]:
    """A synchronous version of search for synchronous code


    See Also
    --------
    :func:`stacksearch.search`

    """
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(search(*args, **kwargs))


async def search(  # TODO: Use logger
    query: str,
    search_on_site: str = "stackoverflow",
) -> Dict[str, List[str]]:
    """Use this. This is the async version of the Search API function.


    Parameters
    ----------
    query : str
        This is the query to search the StackExchange website for.
    search_on_site : str
        The StackExchange website to search on (the default is "stackoverflow").

    Returns
    -------
    Dict[str, List[str]]
        In the format of

        .. code::

            {
                'question': ['answer1', 'answer2', ...], 'question2': ['answer1', ...]
            }

    Raises
    ------
    errors.RateLimitedError
        You got rate limited by StackExchange

    errors.HTMLParseError
        StackExchange has changed their site structure

    errors.RecaptchaError
        StackExchange realizes that we're a bot

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

    def get_answers_and_questions(page: BeautifulSoup) -> Tuple[str, List[str]]:
        try:
            stuff = page("div", attrs=TEXT_REQUIREMENTS)
        except AttributeError as exception:
            raise errors.HTMLParseError(
                "Oh no! It appears that the StackOverflow's question text requirements "
                "have changed. Please go to the Git repository and submit a pull request "
                "to update the TEXT_REQUIREMENTS"
            ) from exception
        return reverse_html(stuff[0]), [reverse_html(answer) for answer in stuff[1:]]

    async with aiohttp.ClientSession() as client:
        ###
        # Get site
        ###
        if not (search_on_site.endswith(".com") or search_on_site.endswith(".org")):
            search_on_site += ".com"

        async with client.get(f"https://{search_on_site}/search?q={query}") as request:
            if request.status == 429:
                raise errors.RateLimitedError(
                    f"You have reached the maximum number of requests to {search_on_site}. Please try again later."
                )

            ###
            # Parse response
            ###

            soup = await soupify(await request.text())
            if soup.find("div", class_="fs-body2 mb24"):  # Captcha test
                raise errors.RecaptchaError(
                    f"{search_on_site} realized that we are not human"
                )

            question_links = await find_questions(soup)

        question_html = []
        for link in map(
            lambda x: f"https://{search_on_site}{x}", iter(question_links.values())
        ):
            time.sleep(random.randint(1, 10) / 100)
            async with client.get(link) as request:
                question_html.append(await request.text())

        pages = [await soupify(page) for page in question_html]

        return dict(map(get_answers_and_questions, pages))
