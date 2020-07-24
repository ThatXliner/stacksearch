#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Bryan Hu .

@Bryan Hu .

Made with love by Bryan Hu .


Version: See __init__.py

Desc: The main file to use/execute when trying to search StackOverflow.

"""

import sys

import argparse
from blessings import Terminal
from pprint import pprint
from . import __version__

try:
    from .Search import Search  # , fSearch
except ModuleNotFoundError:
    try:
        sys.path.insert(0, "..")
        from Search import Search
    except ModuleNotFoundError:
        from gevent import monkey as curious_george

        curious_george.patch_all(thread=False, select=False)
        import requests
        import grequests
        from bs4 import BeautifulSoup as bs
        from typing import Any

        print("Dang it")

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
            _links_for_pages = grequests.map(  # May need to remove this dependancy
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
            full_questions = [
                page.find(attrs=TEXT_REQUIREMENTS).get_text() for page in pages
            ]
            if print_prog:
                print("Identifying answers...")
            answers = [
                [
                    answer.find(attrs=TEXT_REQUIREMENTS).get_text()
                    for answer in page.find_all(
                        attrs={"itemtype": "http://schema.org/Answer"}
                    )
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
parser.add_argument(  # Query
    "query", help="The query to search.", nargs="*", action="extend",
)
parser.add_argument(  # JSON
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
parser.add_argument(  # Output
    "-o",
    "--output",
    help="The output file.",
    nargs="?",
    default=sys.stdout,
    action="store",
    dest="OUTPUT",
)
parser.add_argument(  # Silent
    "-s",
    "--silent",
    action="store_true",
    default=False,
    help="Don't print the progress.",
    dest="s",
)
parser.add_argument(  # Sites
    "--sites",
    action="extend",
    default=["stackoverflow"],
    nargs="+",
    help="The StackExchange sites to search.",
)
parser.add_argument(  # Version
    "-v",
    "-V",
    "--version",
    action="store_true",
    default=False,
    help="Print the version number and exit.",
    dest="version",
)


def main(args: list) -> None:
    """This is the main function for the command-line interface.

    Parameters
    ----------
    args : list
        The list of arguments.

    Returns
    -------
    None
        None

    """

    args = parser.parse_args(args)
    t = Terminal()
    if args.version:
        print(f"stacksearch version: {__version__}")  # noqa
        sys.exit(0)
    elif len(args.query) == 0:
        raise ValueError("Query is required.")
    PRINT_PROGRESS = not args.s
    SITES_TO_SEARCH = set(args.sites)
    if PRINT_PROGRESS:
        print(f"Searching {', '.join(SITES_TO_SEARCH)}...")
    ANSWERS = []
    for site in map(str, SITES_TO_SEARCH):
        ANSWERS.append(
            Search(" ".join(args.query), print_prog=PRINT_PROGRESS, search_on_site=site)
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


if __name__ == "__main__":
    main(sys.argv[1:])
