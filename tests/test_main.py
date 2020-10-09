#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Bryan Hu .

@Bryan Hu .

Made with love by Bryan Hu .


Version: TEST

Desc: YOU SHOULD NOT USE THIS FILE. IT IS A TEST.

"""
import asyncio
from pathlib import Path
from sys import path

path.insert(0, Path(Path(Path(__file__).parent).parent / "stacksearch"))
from stacksearch.__main__ import custom_main as MAIN
from stacksearch.__main__ import fcustom_main as FMAIN
def run(main, *, debug=None):
    """Execute the coroutine and return the result.
    This function runs the passed coroutine, taking care of
    managing the asyncio event loop and finalizing asynchronous
    generators.
    This function cannot be called when another asyncio event loop is
    running in the same thread.
    If debug is True, the event loop will be run in debug mode.
    This function always creates a new event loop and closes it at the end.
    It should be used as a main entry point for asyncio programs, and should
    ideally only be called once.
    Example:
        async def main():
            await asyncio.sleep(1)
            print('hello')
        asyncio.run(main())
    """
    def _cancel_all_tasks(loop):
        to_cancel = asyncio.tasks.all_tasks(loop)
        if not to_cancel:
            return

        for task in to_cancel:
            asyncio.task.cancel()

        loop.run_until_complete(
            asyncio.tasks.gather(*to_cancel, loop=loop, return_exceptions=True))

    for task in to_cancel:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler({
                'message': 'unhandled exception during asyncio.run() shutdown',
                'exception': task.exception(),
                'task': task,
            })
    if asyncio.events._get_running_loop() is not None:
        raise RuntimeError(
            "asyncio.run() cannot be called from a running event loop")

    if not asyncio.coroutines.iscoroutine(main):
        raise ValueError("a coroutine was expected, got {!r}".format(main))

    loop = asyncio.events.new_event_loop()
    try:
        asyncio.events.set_event_loop(loop)
        if debug is not None:
            asyncio.loop.set_debug(debug)
        return asyncio.loop.run_until_complete(main)
    finally:
        try:
            _cancel_all_tasks(loop)
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.run_until_complete(loop.shutdown_default_executor())
        finally:
            asyncio.events.set_event_loop(None)
            loop.close()

class TestClass:
    """For testing."""

    def main(self, args: str = "") -> None:
        """You should not use this. IT'S A TEST. This is the main function."""
        MAIN([arg for arg in args.split() if arg])

    def amain(self, args: str = "") -> None:
        """You should not use this. IT'S A TEST. This is the main async function."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(FMAIN([arg for arg in args.split() if arg]))
        loop.close()

    def test_stable(self):
        """A test with Search."""
        self.main("python list")

    def test_async(self):
        """To test the async search."""
        self.amain("python list")

    def test_stable_lots_of_sites(self):
        """A test with Search. For lots of sites."""
        self.main("python list --sites superuser.com stackoverflow")

    def test_async_lots_of_sites(self):
        """A test with Search. For lots of sites."""
        self.amain("python list --sites superuser.com stackoverflow")

    def test_version(self):
        """To test the version."""
        self.main("-v")

    def test_async_version(self):
        """To test the version."""
        self.amain("-v")

    def test_noobs(self):
        """To test the no argument functionality."""
        self.main()

    def test_async_noobs(self):
        """To test the no argument functionality."""
        self.amain()
