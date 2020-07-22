#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Bryan Hu .

@Bryan Hu .

Made with love by Bryan Hu .


Version: v0.0.1.1

Desc: The main file to use/execute when trying to search StackOverflow.

"""

import argparse
import sys
from blessings import Terminal
import requests
from bs4 import BeautifulSoup as bs

term = Terminal()


def Search(Query: str) -> dict:
    """For getting very precise information on StackOverflow.

    Returns
    -------
    dict
        Description of returned object.

    """
    r = requests.get(f"https://stackoverflow.com/search?q={Query}")
    soup = bs(r.content, "lxml")
    questions = {  # The raw ingredients
        question.string: question.get("href")
        for question in soup.find_all(
            attrs={"class": "question-hyperlink", "data-gps-track": None}
        )
    }
    pages = [  # Pages of all the questions related to Query
        bs(requests.get(link).content, "lxml")
        for link in map(
            lambda x: "https://stackoverflow.com" + x, iter(questions.values())
        )
    ]
    full_questions = [
        page.find(attrs={"class": "post-text", "itemprop": "text"}).get_text()
        for page in pages
    ]
    answers = [
        [
            answer.get_text()
            for answer in page.find_all(attrs={"itemtype": "http://schema.org/Answer"})
        ]
        for page in pages
    ]
    output = dict(zip(full_questions, answers))
    return output


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
parser.add_argument("query", help="The query to search.", nargs="+")
parser.add_argument(
    "-j",
    "--json",
    "--raw-data",
    "-r",
    "--raw",
    help="For outputting JSON data that you can use.",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-o", "--output", help="The output file", nargs="?", default=sys.stdout
)
args = parser.parse_args(sys.argv[1:])
ANSWERS = Search(args.query)
if args.json:
    print(ANSWERS)
else:  # We got some parsing to do
    for question, answer in ANSWERS:
        pass
