#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Bryan Hu .

@Bryan Hu .

Made with love by Bryan Hu .


Version: v1.0.0.1

Desc: The main file to use/execute when trying to search StackOverflow.

"""
from gevent import monkey as curious_george

curious_george.patch_all(thread=False, select=False)

import argparse
import sys
from blessings import Terminal
import requests
import grequests
from bs4 import BeautifulSoup as bs
from typing import Any


# from pprint import pprint

t = Terminal()
NEWLINE = "\n"
TEXT_REQUIREMENTS = {"class": "post-text", "itemprop": "text"}


async def FastSearch(Query: str, *args: Any, **kwargs: Any) -> dict:
    """For getting very precise information on StackOverflow.

    This is 'supposed' to be faster than the normal 'Search' function for it abuses
    Asyncio. The thing is, this function will probably be deprecated unless there is a
    tested significant difference in performance. Use the 'search' function for it is
    more supported (all of the new features will be implemented in the Search function
    first).

    Returns
    -------
    dict
        A dict containing the raw data of the questions/answers gotten.

    """

    async def _full_questions(pages):
        print("Identifying question text...")
        return [page.find(attrs=TEXT_REQUIREMENTS).get_text() for page in pages]

    async def _answers(pages):
        print("Identifying answers...")
        return [
            [
                answer.find(attrs=TEXT_REQUIREMENTS).get_text()
                for answer in page.find_all(
                    attrs={"itemtype": "http://schema.org/Answer"}
                )
            ]
            for page in pages
        ]

    async def parsePages(_links_for_pages):
        return [  # Pages of all the questions related to Query
            bs(link.content, "lxml") for link in _links_for_pages
        ]

    print("Requesting results from StackOverflow...")
    r = requests.get(f"https://stackoverflow.com/search?q={Query}")
    print("Parsing response HTML...")
    soup = bs(r.content, "lxml")
    print("Collecting question links...")
    questions = {  # The raw ingredients
        question.string: question.get("href")
        for question in soup.find_all(
            attrs={"class": "question-hyperlink", "data-gps-track": None}
        )
    }
    print("Requesting questions found...")
    _links_for_pages = grequests.map(
        (
            grequests.get(link)
            for link in map(
                lambda x: "https://stackoverflow.com" + x, iter(questions.values())
            )
        )
    )
    print("Parsing questions found...")
    pages = await parsePages(_links_for_pages)
    full_questions = await _full_questions(pages)
    answers = await _answers(pages)

    return dict(zip(full_questions, answers))


def Search(Query: str, *args: Any, **kwargs: Any) -> dict:
    """For getting very precise information on StackOverflow.

    Returns
    -------
    dict
        A dict containing the raw data of the questions/answers gotten.

    """

    print("Requesting results from StackOverflow...")
    r = requests.get(f"https://stackoverflow.com/search?q={Query}")
    print("Parsing response HTML...")
    soup = bs(r.content, "lxml")
    print("Collecting question links...")
    questions = {  # The raw ingredients
        question.string: question.get("href")
        for question in soup.find_all(
            attrs={"class": "question-hyperlink", "data-gps-track": None}
        )
    }
    print("Requesting questions found...")
    _links_for_pages = grequests.map(
        (
            grequests.get(link)
            for link in map(
                lambda x: "https://stackoverflow.com" + x, iter(questions.values())
            )
        )
    )
    print("Parsing questions found...")
    pages = [  # Pages of all the questions related to Query
        bs(link.content, "lxml") for link in _links_for_pages
    ]
    print("Identifying question text...")
    full_questions = [page.find(attrs=TEXT_REQUIREMENTS).get_text() for page in pages]
    print("Identifying answers...")
    answers = [
        [
            answer.find(attrs=TEXT_REQUIREMENTS).get_text()
            for answer in page.find_all(attrs={"itemtype": "http://schema.org/Answer"})
        ]
        for page in pages
    ]
    return dict(zip(full_questions, answers))


"""
We don't need the internal search function, yet.

def _search(Query: str, *args: Any, **kwargs: Any) -> dict:
    \"""You should never use this. This is the internal search function.

    Returns
    -------
    dict
        A dict containing the raw data of the questions/answers gotten.

    \"""

    print("Requesting results from StackOverflow...")
    r = requests.get(f"https://stackoverflow.com/search?q={Query}")
    print("Parsing response HTML...")
    soup = bs(r.content, "lxml")
    print("Collecting question links...")
    questions = {  # The raw ingredients
        question.string: question.get("href")
        for question in soup.find_all(
            attrs={"class": "question-hyperlink", "data-gps-track": None}
        )
    }
    print("Requesting questions found...")
    _links_for_pages = grequests.map(
        (
            grequests.get(link)
            for link in map(
                lambda x: "https://stackoverflow.com" + x, iter(questions.values())
            )
        )
    )
    print("Parsing questions found...")
    pages = [  # Pages of all the questions related to Query
        bs(link.content, "lxml") for link in _links_for_pages
    ]
    print("Identifying question text...")
    full_questions = [page.find(attrs=TEXT_REQUIREMENTS).get_text() for page in pages]
    print("Identifying answers...")
    answers = [
        [
            answer.find(attrs=TEXT_REQUIREMENTS).get_text()
            for answer in page.find_all(attrs={"itemtype": "http://schema.org/Answer"})
        ]
        for page in pages
    ]
    return dict(zip(full_questions, answers))
"""

parser = argparse.ArgumentParser(
    prog="StackSearch",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
For searching StackOverflow and getting results that you can use.

There are many other libraries/modules available that do the same
thing. The reason you should use this is because this returns results that you can
use. If ran from the command line, it'll return human readable results. If ran from
another python script, it'll return some parsable JSON. Assuming you are utilizing
this script's wonderful functions and objects.""",
    epilog=' \n Judge a man by his questions rather than by his answers" - Voltaire \n ',
)
parser.add_argument("query", help="The query to search.", nargs="+", action="extend")
parser.add_argument(
    "-j",
    "--json",
    "--raw-data",
    "-r",
    "--raw",
    help="For outputting JSON data that you can use.",
    action="store_true",
    default=False,
    dest="json",
)
parser.add_argument(
    "-o",
    "--output",
    help="The output file",
    nargs="?",
    default=sys.stdout,
    action="store",
    dest="OUPUT",
)

args = parser.parse_args(sys.argv[1:])
print("Searching StackOverflow...")
ANSWERS = Search(args.query)

if args.json:
    print(ANSWERS)  # You may get unprocessed, raw JSON
else:  # We got some parsing to do
    print("Outputting results")
    question_number = 1
    for question, answers in ANSWERS.items():
        print(
            f"{t.bold}{t.bright_green}Question #{question_number}: {question}{t.normal}"
        )
        print("\n")
        try:
            print(f"{t.bright_yellow}{t.bold} Best Answer: {answers[0]}{t.normal}")
            print("\n\n\n")
            try:
                for answer in answers[1:]:
                    print(f"{t.green}Answer: {answer}{t.normal}")
                    print("\n\n\n")
            except IndexError:
                print(f"{t.red}{t.bold}This is the only answer.{t.normal}")
        except IndexError:
            print(f"{t.bright_red}There were no answers for this question{t.normal}\n")
        else:
            print("\n\n\n")
        finally:
            question_number += 1
