<h1 align="center">stacksearch 🔎</h1>

<p align="center">
<a href="https://travis-ci.com/ThatXliner/stacksearch"> <img src="https://travis-ci.com/ThatXliner/stacksearch.svg?branch=Stable" alt="Build Status"> </a>
<a href="https://github.com/psf/black"> <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"> </a>
<img src="https://img.shields.io/github/languages/code-size/ThatXliner/stacksearch" alt="GitHub code size in bytes">
<img src="https://img.shields.io/pypi/v/stacksearch" alt="PyPI">
<img src="https://img.shields.io/pypi/implementation/stacksearch" alt="PyPI - Implementation">
<img src="https://img.shields.io/pypi/pyversions/stacksearch" alt="PyPI - Python Version">
<img src="https://img.shields.io/pypi/l/stacksearch" alt="PyPI - License">
<img src="https://img.shields.io/github/languages/top/ThatXliner/stacksearch" alt="GitHub top language">
<img src="https://img.shields.io/github/languages/count/ThatXliner/stacksearch" alt="GitHub language count">
<a href="https://stacksearch.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/stacksearch/badge/?version=latest" alt="Documentation Status"></a>
<a href="https://codecov.io/gh/ThatXliner/stacksearch"> <img src="https://codecov.io/gh/ThatXliner/stacksearch/branch/Stable/graph/badge.svg" /> </a>
</p>


StackSearch is a python module that provides a way to search [StackOverflow](https://stackoverflow.com/).

The reason this is better than other modules is that this module provides a modern API, a beautiful command-line interface via argparse and blessings, all in pure Python.

It is also available as a standalone command-line tool, so you may run it directly like so:

```bash
stacksearch This is the query
```

without the `python3 -m` prefix, if desired.

It also has an API which you can use via

```python
>>> from stackoverflow import Search
>>> Search.Search("This is the query")
```

Have fun!

## Benefits 👍

The benefits of this module as opposed to the other StackOverflow-searching modules is that this module provides the following:

- The ability to return a dictionary of _ALL_ the search results found, **not just the first result**
- The ability to return results from a variety of different [StackExchange](https://stackexchange.com/) sites
- A **beautiful command-line interface _for humans_**
- A decently documented API
- An optional **asynchronous API**
- Decently easy-to-read code (formatted with [Black](https://github.com/psf/black))
- And **open source code on [GitHub](https://github.com/ThatXliner/stacksearch/tree/Stable)**

## Downsides 👎

- Possibly _slower_ than the other modules
- **The first PyPi project ever made by ThatXliner**
- Not _fully_ (completely) optimized (well, after all, it's python)
- ~~A big list of dependencies~~ (shortened in version 1.0.0 or so)

## Current Features 😁

- **Everything listed in the 'Benefits' section of the README above**
- Mostly, **if not fully**, [type-hinted](https://www.python.org/dev/peps/pep-0585/)
- A **beautiful, simple, yet powerful command-line interface** (via [argparse](https://docs.python.org/3/library/argparse.html) and [blessings](https://pypi.org/project/blessings/))
- **Asynchronous** StackOverflow requests!
- The ability to **crank out raw [JSON](https://www.json.org/json-en.html) data** to **_use_**
- And an **API**

## Future Features 🏃‍♂️

- [x] ~~Asynchronous StackOverflow requests!~~ (Done in v1.1.0)
- [x] [Documentation](https://stacksearch.readthedocs.io/en/latest/) (_Sort of_ added in v1.2.8)
- [ ] Object-oriented APIs
- [ ] Python backwards-compatibility
- [ ] Being able to scrape _all_ StackOverflow sites/pages
- [x] ~~A better README~~ (Done in v1.0.0.1)
- [ ] Being able to output different formats of data (e.g. YAML, TOML, XML, etc)
- [ ] And more command-line options

## Usage Examples

- For creating a text editor extension built on this package

- For searching StackOverflow and/or **other StackExchange websites** without leaving the Terminal (for those [Vim](https://www.vim.org/) people)

- For getting lots of answers from all StackExchange sites you know

## License

MIT License

```text
Copyright (c) 2020 ThatXliner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Code style guide 😳

[Black](https://github.com/psf/black). We (I, right now.) use the black formatter to format our code. **It's pretty strict.**

We also use NumPy style docstrings.

## Contributing ✏️

![GitHub contributors](https://img.shields.io/github/contributors/ThatXliner/stacksearch)

Please feel free to contribute!

## Links 📎

[GitHub](https://github.com/ThatXliner/stacksearch/tree/Stable) (Possibly this page)

[PyPi](https://pypi.org/project/stacksearch/) (Possibly this page)

[Travis-CI](https://travis-ci.com/github/ThatXliner/stacksearch)
