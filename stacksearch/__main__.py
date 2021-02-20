#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# type: ignore
"""The main CLI entry point"""
import argparse
import json
import sys
from typing import Dict, List, NoReturn

import rich
import rich.console
import rich.markdown
import rich.markup

from . import __version__, errors, sync_search

parser = argparse.ArgumentParser(
    prog="StackSearch",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""For searching StackExchange and getting results that you can use.""",
    epilog=' \n Judge a man by his questions rather than by his answers" - Voltaire \n ',
)

parser.add_argument(  # Query
    "query", help="The query to search for.", nargs="?", default=None
)
parser.add_argument(  # JSON
    "-j",
    "--json",
    "--raw-data",
    "-r",
    "--raw",
    help="Output JSON instead?",
    action="store_true",
    dest="raw",
)
parser.add_argument(  # Silent
    "-s",
    "--silent",
    action="store_true",
    help="Don't print the progress.",
)

parser.add_argument(  # Sites
    "--sites",
    default=["stackoverflow"],
    nargs="+",
    help="The StackExchange sites to search.",
)
parser.add_argument(  # Version
    "--version", action="version", version="%(prog)s version: " + __version__
)
parser.add_argument(
    "--pager", action="store_true", help="Use a pager for output (may turn color off)"
)
parser.add_argument(
    "--pager-colors",
    action="store_true",
    help="Force colors when the --pager option is also specified",
)

console = rich.console.Console()


def main() -> NoReturn:
    """The main entry point"""
    args = parser.parse_args()

    if args.query is None or args.query == "":
        parser.print_help()
    else:
        sites = set(args.sites)
        try:
            with console.status(f"Searching {', '.join(sites)}\n"):
                returned_data = {
                    site: sync_search(args.query, search_on_site=site) for site in sites
                }
        except errors.RecaptchaError as error:
            raise error
        except errors.StackSearchBaseError as error:
            console.print(rich.markup.escape(repr(error)), style="bold red")
            sys.exit(1)
        if args.raw:
            print(json.dumps(returned_data))
            sys.exit(0)

        def print_questions_and_answers(data: Dict[str, Dict[str, List[str]]]):
            for site, questions in data.items():
                console.rule(f"[bold]Site: [blue]{site}[/]\n\n")
                for question, answers in questions.items():
                    console.rule("Question")
                    console.print(rich.markdown.Markdown(question))
                    console.rule("Answer(s)")
                    if len(answers) == 0:
                        console.print(
                            "[bold red]There were no answers for this question[/]"
                        )
                    else:
                        for index, answer in enumerate(answers):
                            console.rule(f"Answer [yellow]#{index}[/]", align="left")
                            console.print(rich.markdown.Markdown(answer))

        if args.pager:
            with console.pager(styles=args.pager_colors):
                print_questions_and_answers(returned_data)
        else:
            print_questions_and_answers(returned_data)


if __name__ == "__main__":
    main()
