===============================
Quickstart guide
===============================

So, you've seen it on PyPi, you've noticed it on GitHub, and now want to know how to use ``stacksearch``? This quickstart guide will help you understand most of the features of stacksearch. It'll cover basic usage, options, and some of the API features. So, without further ado, let's dive in!

Installation
----------------

.. warning::
   To install stacksearch, **you must have python version 3.8 or higher**.
   The reason for this is because ``stacksearch`` requires this feature of ``argparse`` that **no other python version supports.**

You can easily install ``stacksearch`` via ``pip``:

``pip install stacksearch``

or

``python3.8 -m install stacksearch``

or you can install it manually via ``git clone``:

.. code-block:: bash

   mkdir stacksearch
   git clone https://github.com/ThatXliner/stacksearch.git

Whatever you prefer.

.. note::
   If you want to install stacksearch via git, make sure to install the latest *stable* version


Basic Tasks
----------------

``stacksearch`` is designed so that *anyone can use it, with ease.*

To refer to the commands ``stacksearch`` provides (or the help menu), you can type ``stacksearch --help`` or ``stacksearch -h``.

To search StackOverflow directly from the command-line, do ``stacksearch this is your query`` or ``python3.8 -m stacksearch this is your query`` and replace 'this is your query' with the query string you want to search for.

.. note:: For the rest of this tutorial, we'll refer your preferred stacksearch command as stacksearch for simplicity



Options
----------------

You can also provide *additional* options to ``stacksearch``.

For example, say you want to search *all* of the StackExchange you know, then you would run ``stacksearch this is your query --sites ...`` (replace '...' with the sites you want to search)

Or maybe you just don't want so much debug information filling up your terminal, then you can pass the `--silent` option. Which could also be shortened to `-s`.

.. warning:: DO NOT CONFUSE THE ``-s`` OPTION WITH THE ``--sites`` OPTION! THEY ARE NOT THE SAME!!

Or *maybe* you want JSON output that *you* can use. Then you can pass the ``--json`` option, the ``-j`` option, the ``--raw-data`` option, the ``--raw`` option, or the ``-r`` option. It'll output raw JSON data instead of beautifully formatted (and elegantly colorized) question-and-answers.

.. note:: The feature mentioned above may be subject to change

Simple API
----------------

.. seealso::

   :doc:`api-ref`

An example of how simple stacksearch's API is:

.. code-block:: python
   :linenos:
   :caption: To prove how simple, yet powerful, stacksearch is

   from stacksearch.Searcher import Search
   print(Search("How do i code python"))

And then, from just 2 lines of code, you can effectively search for answers on StackOverflow using the simple stacksearch API.

But, if you want to search for multiple questions *asynchronously*, you can use the asynchronous stacksearch API instead:

.. code-block:: python
   :linenos:
   :caption: This is the asynchronous stacksearch API

   from stacksearch.Searcher import fSearch
   import asyncio
   async def main():
       stuff = []
       stuff.append(await fSearch('How do i code python'))
       stuff.append(await fSearch('How do make my own object'))
       stuff.append(await fSearch('What are objects'))
       stuff.append(await fSearch('[python] lists'))
       return stuff
   print(asyncio.run(main))

If you want to.

.. note:: The asynchronous API is only decently stable. The StackExchange server may stop requests from too much asynchronous operations.
