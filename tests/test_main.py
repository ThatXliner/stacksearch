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
import random
from typing import Any, Awaitable, Coroutine, List, TypeVar, Union

from stacksearch.__main__ import custom_main as MAIN
from stacksearch.__main__ import fcustom_main as FMAIN

_T = TypeVar("_T")


def run(
    main: Union[Coroutine[Any, None, _T], Awaitable[_T]], *, debug: bool = False
) -> _T:
    """Run a coroutine.

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
    import weakref

    try:
        from asyncio import get_running_loop  # noqa Python >=3.7
    except ImportError:  # pragma: no cover
        from asyncio.events import (
            _get_running_loop as get_running_loop,
        )  # pragma: no cover

    def _cancel_all_tasks(loop, tasks):
        to_cancel = [task for task in tasks if not task.done()]

        if not to_cancel:
            return

        for task in to_cancel:
            task.cancel()

        loop.run_until_complete(
            asyncio.gather(*to_cancel, loop=loop, return_exceptions=True)
        )

        for task in to_cancel:
            if task.cancelled():
                continue
            if task.exception() is not None:
                loop.call_exception_handler(
                    {
                        "message": "unhandled exception during asyncio.run() shutdown",
                        "exception": task.exception(),
                        "task": task,
                    }
                )

    def _patch_loop(loop):
        """
        This function is designed to work around https://bugs.python.org/issue36607

        It's job is to keep a thread safe variable tasks up to date with any tasks that
        are created for the given loop. This then lets you cancel them as _all_tasks
        was intended for.

        We also need to patch the {get,set}_task_factory functions because we can't allow
        Other users of it to overwrite our factory function. This function will pretend
        like there is no factory set but in reality our factory is always set and we will
        call the provided one set
        """
        tasks = weakref.WeakSet()

        task_factory = [None]

        def _set_task_factory(factory):
            task_factory[0] = factory

        def _get_task_factory():
            return task_factory[0]

        def _safe_task_factory(loop, coro):
            if task_factory[0] is None:
                # These lines are copied from the standard library because they don't have
                # this inside a default factory function for me to call.
                # https://github.com/python/cpython/blob/3.6/Lib/asyncio/base_events.py#L304
                task = asyncio.Task(coro, loop=loop)
                if task._source_traceback:
                    del task._source_traceback[-1]  # pragma: no cover
            else:
                task = task_factory[0](loop, coro)
            tasks.add(task)
            return task

        loop.set_task_factory(_safe_task_factory)
        loop.set_task_factory = _set_task_factory
        loop.get_task_factory = _get_task_factory

        return tasks

    # Python 3.7+ raises RuntimeError while <3.6 returns None
    try:
        loop = get_running_loop()
    except RuntimeError:
        loop = None
    if loop is not None:
        raise RuntimeError("asyncio.run() cannot be called from a running event loop")

    if not asyncio.iscoroutine(main):
        raise ValueError("a coroutine was expected, got {!r}".format(main))

    loop = asyncio.new_event_loop()
    tasks = _patch_loop(loop)

    try:
        asyncio.set_event_loop(loop)
        loop.set_debug(debug)
        return loop.run_until_complete(main)
    finally:
        try:
            _cancel_all_tasks(loop, tasks)
            loop.run_until_complete(loop.shutdown_asyncgens())
        finally:
            asyncio.set_event_loop(None)  # type: ignore
            loop.close()


def _get_random_sites() -> List[str]:
    SITES = [
        "stackoverflow.com",
        "serverfault.com",
        "superuser.com",
        "meta.stackexchange.com",
        "webapps.stackexchange.com",
        "webapps.meta.stackexchange.com",
        "gaming.stackexchange.com",
        "gaming.meta.stackexchange.com",
        "webmasters.stackexchange.com",
        "webmasters.meta.stackexchange.com",
        "cooking.stackexchange.com",
        "cooking.meta.stackexchange.com",
        "gamedev.stackexchange.com",
        "gamedev.meta.stackexchange.com",
        "photo.stackexchange.com",
        "photo.meta.stackexchange.com",
        "stats.stackexchange.com",
        "stats.meta.stackexchange.com",
        "math.stackexchange.com",
        "math.meta.stackexchange.com",
        "diy.stackexchange.com",
        "diy.meta.stackexchange.com",
        "meta.superuser.com",
        "meta.serverfault.com",
        "gis.stackexchange.com",
        "gis.meta.stackexchange.com",
        "tex.stackexchange.com",
        "tex.meta.stackexchange.com",
        "askubuntu.com",
        "meta.askubuntu.com",
    ]
    return set([random.choice(SITES) for x in range(random.randint(1, 3))])


class TestClass:
    """For testing."""

    def main(self, args: str = "") -> None:
        """You should not use this. IT'S A TEST. This is the main function."""
        MAIN([arg for arg in args.split() if arg])

    def amain(self, args: str = "") -> None:
        """You should not use this. IT'S A TEST. This is the main async function."""
        run(FMAIN([arg for arg in args.split() if arg]))

    def test_stable(self):
        """A test with Search."""
        self.main("python list")

    def test_async(self):
        """To test the async search."""
        self.amain("python list")

    def test_stable_lots_of_sites(self):
        """A test with Search. For lots of sites."""
        self.main(f"python list --sites {' '.join(_get_random_sites())}")

    def test_async_lots_of_sites(self):
        """A test with Search. For lots of sites."""
        self.amain(f"python list --sites {' '.join(_get_random_sites())}")

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
