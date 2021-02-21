<h1 align="center">stacksearch 🔎</h1>

<p align="center">
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
    <a href="https://pypi.org/project/stacksearch/"><img src="https://img.shields.io/pypi/v/stacksearch" alt="PyPI"></a>
    <a href="https://pypi.org/project/stacksearch/"><img src="https://img.shields.io/pypi/pyversions/stacksearch" alt="PyPI - Python Version"></a>
    <a href="https://pypi.org/project/stacksearch/"><img src="https://img.shields.io/pypi/l/stacksearch" alt="PyPI - License"></a>
    <a href="https://stacksearch.readthedocs.io/en/latest/"><img src="https://readthedocs.org/projects/stacksearch/badge/?version=latest" alt="Documentation Status"></a>
    <a href="https://github.com/ThatXliner/stacksearch/actions/workflows/python-check.yml"><img src="https://github.com/ThatXliner/stacksearch/actions/workflows/python-check.yml/badge.svg" alt="PythonCI"></a>
    <a href="https://codecov.io/gh/ThatXliner/stacksearch"> <img src="https://codecov.io/gh/ThatXliner/stacksearch/branch/master/graph/badge.svg" /> </a>
</p>

**NOTE: STACKSEARCH IS NO LONGER ACTIVELY MAINTAINED. There will still be the occasional bug fixes and updates, but not as much.**


StackSearch is a python module that provides a way to search [StackExchange](https://stackexchange.com) sites such as [StackOverflow](https://stackoverflow.com).

## Installation

You know the drill

```bash
$ pip install stacksearch
```
## Usage
### CLI

```bash
$ stacksearch "This is the query"
```
or
```bash
$ python3 -m stacksearch "This is the query"
```
### Python API

```python
>>> from stacksearch import sync_search
>>> sync_search("This is the query")
```
or the asynchronous version

```python
>>> import asyncio
>>> from stacksearch import search
>>> async def main():
...    await search("This is the query")

>>> asyncio.run(main())
```
Have fun!

## Features

The benefits of this module as opposed to the other StackOverflow-searching modules is that this module provides the following:

- A **markdown reverser engine** via [unmarkd](https://github.com/ThatXliner/unmarkd) to return useful and beautiful answers
- The ability to return a dictionary of _ALL_ the search results found, **not just the first result**
- The ability to return results from all [StackExchange](https://stackexchange.com/) sites
- A **beautiful command-line interface _for humans_** via [argparse](https://docs.python.org/3/library/argparse.html) and [**Rich**](https://github.com/willmcgugan/rich)
- An optional **asynchronous Python API**
- The ability to **crank out raw [JSON](https://www.json.org/json-en.html) data** to use
- Fully [type hinted](https://www.python.org/dev/peps/pep-0585/)


## Usage Examples

- For creating a text editor extension built on this package

- For searching StackOverflow and/or **other StackExchange websites** without leaving the Terminal (for those [Vim](https://www.vim.org/) people)

- For getting lots of answers from all StackExchange sites you know

## License

[MIT](https://choosealicense.com/licenses/mit/)

Please feel free to contribute!

## Links 📎

 - [GitHub](https://github.com/ThatXliner/stacksearch/tree/Stable)
 - [PyPi](https://pypi.org/project/stacksearch/)
