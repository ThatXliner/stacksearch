===============================
Quickstart guide
===============================

So, you've seen it on PyPi, you've noticed it on GitHub, and now want to know how to use ``stacksearch``? This quickstart guide will help you understand most of the features of stacksearch. It'll cover basic usage, options, and some of the API features. So, without further ado, let's dive in!

Installation
----------------

To install stacksearch, **you must have python version 3.8 or higher**.

The reason for this is because ``stacksearch`` requires this feature of ``argparse`` that **no other python version supports.**

You can easily install ``stacksearch`` via ``pip```:

``` pip install stacksearch ```

or

```python3.8 -m install stacksearch```

or you can install it manually via ``git clone``:

```mkdir stacksearch```
```git clone https://github.com/ThatXliner/stacksearch.git```

Whatever you prefer.


Basic Tasks
----------------

``stacksearch`` is designed so that *anyone can use it, with **ease**.*

To refer to the commands ``stacksearch`` provides (or the help menu), you can type `stacksearch --help` or ``stacksearch -h``.

To search StackOverflow directly from the command-line, do ``stacksearch this is your query`` or ``python3.8 -m stacksearch this is your query`` and replace 'this is your query' with the query string you want to search for.

**NOTE: For the rest of this tutorial, we'll refer your preferred ``stacksearch`` command as ``stacksearch`` for simplicity.**

.. |python logo| image:: resource/py-logo.svg


Extra options
----------------

You can also provide *additional* options to `stacksearch`.

For example, say you want to search *all* of the StackExchange you know, then you would run `stacksearch this is your query --sites ...` (replace '...' with the sites you want to search)

Or maybe you just don't want so much debug information filling up your terminal, then you can pass the `--silent` option. Which could also be shortened to `-s`.

**WARNING! DO NOT CONFUSE THE `-s` OPTION WITH THE `--sites` OPTION! THEY ARE NOT THE SAME!!**

Or *maybe* you want JSON output that *you* can use. Then you can pass the `--json` option, the `-j` option, the `--raw-data` option, the `--raw` option, or the `-r` option. It'll output raw JSON data instead of beautifully formatted (and elegantly colorized) question-and-answers.

**NOTE: The feature mentioned above is subject to change (after all, this *is* alpha)**
