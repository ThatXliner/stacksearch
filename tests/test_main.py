#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Bryan Hu .

@Bryan Hu .

Made with love by Bryan Hu .


Version: v1.1.0.1

Desc: The main file to use/execute when trying to search StackOverflow.

"""
from gevent import monkey as curious_george

curious_george.patch_all(thread=False, select=False)

import sys
import argparse
import requests
import grequests
import pytest

# import asyncio
from bs4 import BeautifulSoup as bs
from blessings import Terminal
from pprint import pprint
from typing import Any


t = Terminal()
# NEWLINE = "\n"
# TEXT_REQUIREMENTS = {"class": "post-text", "itemprop": "text"}

# TODO: In the future, remove the gevent/grequests dependency.
# TODO: In the future, add tests against 0-question results
# TODO: In the future, add tests against invalid sites. Also, process the sites.
# TODO: In the future, add tests against offline.


def _remove_dot_com(string: str) -> str:
    string = str(string)
    # Maybe a regex is better here...
    if string.endswith(".com"):
        return string[0 : len(string) - 4]
    elif string.endswith(".org"):
        return string[0 : len(string) - 4]
    else:
        return string


async def fSearch(
    Query: str,
    print_prog: bool = True,
    search_on_site: str = "stackoverflow",
    # Including the "stackexchange.com" (if present) but not the ".com" suffix
    *args: Any,
    **kwargs: Any,
) -> dict:
    """For getting very precise information on StackOverflow. The async (awaitable) version.

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

    async def _remove_dot_com(string: str) -> str:
        if string.endswith(".com"):
            return string[0 : len(string) - 4]

    search_on_site = await _remove_dot_com(search_on_site)
    TEXT_REQUIREMENTS = {"class": "post-text", "itemprop": "text"}

    async def _full_questions(pages):
        if print_prog:
            print("Identifying question text...")
        return [page.find(attrs=TEXT_REQUIREMENTS).get_text() for page in pages]

    async def _answers(pages):
        if print_prog:
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

    if print_prog:
        print(f"Requesting results from {search_on_site}...")
    r = requests.get(
        f"https://{search_on_site}/search?q={Query}"
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
    _links_for_pages = grequests.map(
        (
            grequests.get(link)
            for link in map(
                lambda x: f"https://{search_on_site}" + x,
                iter(
                    questions.values()
                ),  # NOTE: For python3.9, use str.remove_suffix()
            )
        )
    )
    if print_prog:
        print("Parsing questions found (This may take a while)...")
    pages = await parsePages(_links_for_pages)
    full_questions = await _full_questions(pages)
    answers = await _answers(pages)

    return dict(zip(full_questions, answers))


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
    search_on_site = _remove_dot_com(str(search_on_site))
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
    _links_for_pages = grequests.map(
        (
            grequests.get(link)
            for link in map(
                lambda x: f"https://{search_on_site}.com" + x,
                iter(
                    questions.values()
                ),  # NOTE: For python3.9, use str.remove_suffix()
            )
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
    help="The output file.",
    nargs="?",
    default=sys.stdout,
    action="store",
    dest="OUTPUT",
)
parser.add_argument(
    "-s",
    "--silent",
    action="store_true",
    default=False,
    help="Don't print the progress.",
    dest="s",
)
parser.add_argument(
    "--sites",
    action="extend",
    default=["stackoverflow"],
    nargs="+",
    help="The StackExchange sites to search.",
)
parser.add_argument(
    "-v",
    "-V",
    "--version",
    action="store_true",
    default=False,
    help="Print the version number and exit.",
    dest="version",
)


class TestClass:
    """For testing."""

    def test_one(self):
        """A test with Search."""
        args = parser.parse_args("python list".split())
        if args.version:
            print(f"stacksearch version: {__version__}")  # noqa
            sys.exit(0)
        PRINT_PROGRESS = not args.s
        SITES_TO_SEARCH = set(map(_remove_dot_com, args.sites))
        if PRINT_PROGRESS:
            print(f"Searching {', '.join(SITES_TO_SEARCH)}...")
        ANSWERS = []
        for site in map(str, SITES_TO_SEARCH):
            ANSWERS.append(
                Search(
                    " ".join(args.query), print_prog=PRINT_PROGRESS, search_on_site=site
                )
            )

        if args.json:
            pprint(
                ANSWERS, stream=args.OUTPUT, width=79
            )  # You will get unprocessed, raw JSON
        else:  # We got some parsing to do
            if PRINT_PROGRESS:
                print("Outputting results")

            for answer in ANSWERS:
                question_number = 1
                print(t.bold("Answers from {}"))
                for question, answers in answer.items():
                    print(
                        f"{t.bold}{t.bright_green}Question #{question_number}: {question}{t.normal}",
                        file=args.OUTPUT,
                    )
                    print("\n")
                    try:
                        print(
                            f"{t.bright_yellow}{t.bold} Best Answer: {answers[0]}{t.normal}",
                            file=args.OUTPUT,
                        )
                        print("\n\n\n", file=args.OUTPUT)
                        try:
                            for question_answer in answers[1:]:
                                print(
                                    f"{t.green}Answer: {question_answer}{t.normal}",
                                    file=args.OUTPUT,
                                )
                                print("\n\n\n", file=args.OUTPUT)
                        except IndexError:
                            print(
                                f"{t.red}{t.bold}This is the only answer.{t.normal}",
                                file=args.OUTPUT,
                            )
                    except IndexError:
                        print(
                            f"{t.bright_red}There were no answers for this question{t.normal}\n",
                            file=args.OUTPUT,
                        )
                    else:
                        print("\n\n\n", file=args.OUTPUT)
                    finally:
                        question_number += 1

#     @pytest.mark.asyncio
#     async def test_two(self):
#         """A test with the asyncio version of Search."""
#         args = parser.parse_args("python list".split())
#         if args.version:
#             print(f"stacksearch version: {__version__}")  # NOQA
#             sys.exit(0)
#         PRINT_PROGRESS = not args.s
#         SITES_TO_SEARCH = args.sites
#         if PRINT_PROGRESS:
#             print(f"Searching {', '.join(SITES_TO_SEARCH)}...")
#         ANSWERS = []
#         for site in map(str, SITES_TO_SEARCH):
#             ANSWERS.append(
#                 await fSearch(
#                     " ".join(args.query), print_prog=PRINT_PROGRESS, search_on_site=site
#                 )
#             )

#         if args.json:
#             pprint(
#                 ANSWERS, stream=args.OUTPUT, width=79
#             )  # You will get unprocessed, raw JSON
#         else:  # We got some parsing to do
#             if PRINT_PROGRESS:
#                 print("Outputting results")

#             for answer in ANSWERS:
#                 question_number = 1
#                 print(t.bold("Answers from {}"))
#                 for question, answers in answer.items():
#                     print(
#                         f"{t.bold}{t.bright_green}Question #{question_number}: {question}{t.normal}",
#                         file=args.OUTPUT,
#                     )
#                     print("\n")
#                     try:
#                         print(
#                             f"{t.bright_yellow}{t.bold} Best Answer: {answers[0]}{t.normal}",
#                             file=args.OUTPUT,
#                         )
#                         print("\n\n\n", file=args.OUTPUT)
#                         try:
#                             for question_answer in answers[1:]:
#                                 print(
#                                     f"{t.green}Answer: {question_answer}{t.normal}",
#                                     file=args.OUTPUT,
#                                 )
#                                 print("\n\n\n", file=args.OUTPUT)
#                         except IndexError:
#                             print(
#                                 f"{t.red}{t.bold}This is the only answer.{t.normal}",
#                                 file=args.OUTPUT,
#                             )
#                     except IndexError:
#                         print(
#                             f"{t.bright_red}There were no answers for this question{t.normal}\n",
#                             file=args.OUTPUT,
#                         )
#                     else:
#                         print("\n\n\n", file=args.OUTPUT)
#                     finally:
#                         question_number += 1

    def test_one_lots_of_sites(self):
        """A test with Search. For lots of sites."""
        args = parser.parse_args(
            "python list --sites superuser.com stackoverflow".split()
        )
        if args.version:
            print(f"stacksearch version: {__version__}")  # noqa
            sys.exit(0)
        PRINT_PROGRESS = not args.s
        SITES_TO_SEARCH = set(map(_remove_dot_com, args.sites))
        if PRINT_PROGRESS:
            print(f"Searching {', '.join(SITES_TO_SEARCH)}...")
        ANSWERS = []
        for site in map(str, SITES_TO_SEARCH):
            ANSWERS.append(
                Search(
                    " ".join(args.query), print_prog=PRINT_PROGRESS, search_on_site=site
                )
            )

        if args.json:
            pprint(
                ANSWERS, stream=args.OUTPUT, width=79
            )  # You will get unprocessed, raw JSON
        else:  # We got some parsing to do
            if PRINT_PROGRESS:
                print("Outputting results")

            for answer in ANSWERS:
                question_number = 1
                print(t.bold("Answers from {}"))
                for question, answers in answer.items():
                    print(
                        f"{t.bold}{t.bright_green}Question #{question_number}: {question}{t.normal}",
                        file=args.OUTPUT,
                    )
                    print("\n")
                    try:
                        print(
                            f"{t.bright_yellow}{t.bold} Best Answer: {answers[0]}{t.normal}",
                            file=args.OUTPUT,
                        )
                        print("\n\n\n", file=args.OUTPUT)
                        try:
                            for question_answer in answers[1:]:
                                print(
                                    f"{t.green}Answer: {question_answer}{t.normal}",
                                    file=args.OUTPUT,
                                )
                                print("\n\n\n", file=args.OUTPUT)
                        except IndexError:
                            print(
                                f"{t.red}{t.bold}This is the only answer.{t.normal}",
                                file=args.OUTPUT,
                            )
                    except IndexError:
                        print(
                            f"{t.bright_red}There were no answers for this question{t.normal}\n",
                            file=args.OUTPUT,
                        )
                    else:
                        print("\n\n\n", file=args.OUTPUT)
                    finally:
                        question_number += 1

#     @pytest.mark.asyncio
#     async def test_two_lots_of_sites(self):
#         """A test with the asyncio version of Search. For lots of sites."""
#         args = parser.parse_args(
#             "python list --sites superuser.com stackoverflow".split()
#         )
#         if args.version:
#             print(f"stacksearch version: {__version__}")  # noqa
#             sys.exit(0)
#         PRINT_PROGRESS = not args.s
#         SITES_TO_SEARCH = args.sites
#         if PRINT_PROGRESS:
#             print(f"Searching {', '.join(SITES_TO_SEARCH)}...")
#         ANSWERS = []
#         for site in map(str, SITES_TO_SEARCH):
#             ANSWERS.append(
#                 await fSearch(
#                     " ".join(args.query), print_prog=PRINT_PROGRESS, search_on_site=site
#                 )
#             )

#         if args.json:
#             pprint(
#                 ANSWERS, stream=args.OUTPUT, width=79
#             )  # You will get unprocessed, raw JSON
#         else:  # We got some parsing to do
#             if PRINT_PROGRESS:
#                 print("Outputting results")

#             for answer in ANSWERS:
#                 question_number = 1
#                 print(t.bold("Answers from {}"))
#                 for question, answers in answer.items():
#                     print(
#                         f"{t.bold}{t.bright_green}Question #{question_number}: {question}{t.normal}",
#                         file=args.OUTPUT,
#                     )
#                     print("\n")
#                     try:
#                         print(
#                             f"{t.bright_yellow}{t.bold} Best Answer: {answers[0]}{t.normal}",
#                             file=args.OUTPUT,
#                         )
#                         print("\n\n\n", file=args.OUTPUT)
#                         try:
#                             for question_answer in answers[1:]:
#                                 print(
#                                     f"{t.green}Answer: {question_answer}{t.normal}",
#                                     file=args.OUTPUT,
#                                 )
#                                 print("\n\n\n", file=args.OUTPUT)
#                         except IndexError:
#                             print(
#                                 f"{t.red}{t.bold}This is the only answer.{t.normal}",
#                                 file=args.OUTPUT,
#                             )
#                     except IndexError:
#                         print(
#                             f"{t.bright_red}There were no answers for this question{t.normal}\n",
#                             file=args.OUTPUT,
#                         )
#                     else:
#                         print("\n\n\n", file=args.OUTPUT)
#                     finally:
#                         question_number += 1
