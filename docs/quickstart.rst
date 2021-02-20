===============================
Quickstart guide
===============================

This file will show you how to use StackSearch to search StackOverflow

Installation
----------------

.. warning::
   To install stacksearch, **you must have python version 3.6 or higher**.

You can easily install ``stacksearch`` via ``pip``:

``pip install stacksearch``

or

``python -m install stacksearch``


Whatever you prefer.


Basic CLI Tasks
----------------

``stacksearch`` is designed so that *anyone can use it, with ease.*

To refer to the commands ``stacksearch`` provides (or the help menu), you can type ``stacksearch --help`` or ``stacksearch -h``.

To search StackOverflow directly from the command-line, do ``stacksearch "this is your query"`` or ``python -m stacksearch "this is your query"`` and replace ``"this is your query"`` with the query string you want to search for.


Options
----------------

You can also provide *additional* options to ``stacksearch``.

For example, say you want to search *all* of the StackExchange you know, then you would run ``stacksearch this is your query --sites ...`` (replace '...' with the sites you want to search)

Or maybe you just don't want so much debug information filling up your terminal, then you can pass the `--silent` option. Which could also be shortened to `-s`.

.. warning:: DO NOT CONFUSE THE ``-s`` OPTION WITH THE ``--sites`` OPTION! THEY ARE NOT THE SAME!!

Or *maybe* you want JSON output that *you* can use in other programs. Then you can pass the ``--json`` option, the ``-j`` option, the ``--raw-data`` option, the ``--raw`` option, or the ``-r`` option instead.

It'll output raw JSON data instead of beautifully formatted (and elegantly colorized)
question-and-answers.

Simple API
----------------

.. seealso::

   :ref:`api-ref`

An example of how to StackSearch's API to search for any StackExchange site is:

.. code:: python

   from stacksearch import sync_search
   print(sync_search("How do i code python"))

And then, from just 2 lines of code, you can effectively search for answers on StackOverflow using the simple stacksearch API.

**Why is it called :func:`stacksearch.sync_search`?**

Well, that's because it's actually a wrapper around the asynchronous API.

If you want to search for multiple questions *asynchronously*, you can use write:

.. code:: python

   from stacksearch import search
   import asyncio
   async def main():
       stuff = []
       stuff.append(await search('How do i code python'))
       stuff.append(await search('How do make my own object'))
       stuff.append(await search('What are objects'))
       stuff.append(await search('[python] lists'))
       return stuff
   print(asyncio.run(main))

If you want to.
