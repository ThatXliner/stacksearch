#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Bryan Hu .

@Bryan Hu .

Made with love by Bryan Hu .


Version: TEST

Desc: The main file to use/execute when trying to search StackOverflow.

"""
from sys import path
from pathlib import Path

path.insert(0, Path(Path(Path(__file__).parent).parent / "stacksearch"))
from stacksearch.__main__ import custom_main as MAIN


class TestClass:
    """For testing."""

    # async def a_main(self, args):
    #     """Async version of a_main.
    #
    #     Returns
    #     -------
    #     None
    #
    #     """
    #     args = parser.parse_args((args).split())
    #     if args.version:
    #         print(f"stacksearch version: {__version__}")  # noqa
    #         sys.exit(0)
    #     PRINT_PROGRESS = not args.s
    #     SITES_TO_SEARCH = set(map(_remove_dot_com, args.sites))
    #     if PRINT_PROGRESS:
    #         print(f"Searching {', '.join(SITES_TO_SEARCH)}...")
    #     ANSWERS = []
    #     for site in map(str, SITES_TO_SEARCH):
    #         ANSWERS.append(
    #             await fSearch(
    #                 " ".join(args.query), print_prog=PRINT_PROGRESS, search_on_site=site
    #             )
    #         )
    #
    #     if args.json:
    #         pprint(
    #             ANSWERS, stream=args.OUTPUT, width=79
    #         )  # You will get unprocessed, raw JSON
    #     else:  # We got some parsing to do
    #         if PRINT_PROGRESS:
    #             print("Outputting results")
    #
    #         for answer in ANSWERS:
    #             question_number = 1
    #             print(t.bold("Answers from {}"))
    #             for question, answers in answer.items():
    #                 print(
    #                     f"{t.bold}{t.bright_green}Question #{question_number}: {question}{t.normal}",
    #                     file=args.OUTPUT,
    #                 )
    #                 print("\n")
    #                 try:
    #                     print(
    #                         f"{t.bright_yellow}{t.bold} Best Answer: {answers[0]}{t.normal}",
    #                         file=args.OUTPUT,
    #                     )
    #                     print("\n\n\n", file=args.OUTPUT)
    #                     try:
    #                         for question_answer in answers[1:]:
    #                             print(
    #                                 f"{t.green}Answer: {question_answer}{t.normal}",
    #                                 file=args.OUTPUT,
    #                             )
    #                             print("\n\n\n", file=args.OUTPUT)
    #                     except IndexError:
    #                         print(
    #                             f"{t.red}{t.bold}This is the only answer.{t.normal}",
    #                             file=args.OUTPUT,
    #                         )
    #                 except IndexError:
    #                     print(
    #                         f"{t.bright_red}There were no answers for this question{t.normal}\n",
    #                         file=args.OUTPUT,
    #                     )
    #                 else:
    #                     print("\n\n\n", file=args.OUTPUT)
    #                 finally:
    #                     question_number += 1

    def main(self, args):
        """You should not use this. IT'S A TEST. This is the main function."""
        MAIN(args)

    def test_one(self):
        """A test with Search."""
        self.main("python list")

    #     @pytest.mark.asyncio
    #     async def test_two(self):
    #         """A test with the asyncio version of Search."""
    #         self.a_main("python list")

    def test_one_lots_of_sites(self):
        """A test with Search. For lots of sites."""
        self.main("python list --sites superuser.com stackoverflow")

    #     @pytest.mark.asyncio
    #     async def test_two_lots_of_sites(self):
    #         """A test with the asyncio version of Search. For lots of sites."""
    #           self.a_main("python list --sites superuser.com stackoverflow")
    def test_version(self):
        """To test the version."""
        self.main("-v")
