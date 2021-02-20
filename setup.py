# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stacksearch']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'rich>=9.11.0,<10.0.0']

entry_points = \
{'console_scripts': ['stacksearch = stacksearch.__main__:main']}

setup_kwargs = {
    'name': 'stacksearch',
    'version': '1.5',
    'description': 'StackSearch is a python CLI and library that provides a way to search StackExchange sites.',
    'long_description': '<h1 align="center">stacksearch 🔎</h1>\n\n<p align="center">\n    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>\n    <a href="https://pypi.org/project/stacksearch/"><img src="https://img.shields.io/pypi/v/stacksearch" alt="PyPI"></a>\n    <a href="https://pypi.org/project/stacksearch/"><img src="https://img.shields.io/pypi/pyversions/stacksearch" alt="PyPI - Python Version"></a>\n    <a href="https://pypi.org/project/stacksearch/"><img src="https://img.shields.io/pypi/l/stacksearch" alt="PyPI - License"></a>\n    <a href="https://stacksearch.readthedocs.io/en/latest/"><img src="https://readthedocs.org/projects/stacksearch/badge/?version=latest" alt="Documentation Status"></a>\n    <a href="https://codecov.io/gh/ThatXliner/stacksearch"> <img src="https://codecov.io/gh/ThatXliner/stacksearch/branch/master/graph/badge.svg" /> </a>\n</p>\n\n**NOTE: STACKSEARCH IS NO LONGER ACTIVELY MAINTAINED. There will still be the occasional bug fixes and updates, but not as much.**\n\n\nStackSearch is a python module that provides a way to search [StackOverflow](https://stackoverflow.com/).\n\nThe reason this is better than other modules is that this module provides a modern API, a beautiful command-line interface via argparse and blessings, all in pure Python.\n\nIt is also available as a standalone command-line tool, so you may run it directly like so:\n\n```bash\nstacksearch This is the query\n```\n\nwithout the `python3 -m` prefix, if desired.\n\nIt also has an API which you can use via\n\n```python\n>>> from stackoverflow import Search\n>>> Search.Search("This is the query")\n```\n\nHave fun!\n\n## Benefits 👍\n\nThe benefits of this module as opposed to the other StackOverflow-searching modules is that this module provides the following:\n\n- The ability to return a dictionary of _ALL_ the search results found, **not just the first result**\n- The ability to return results from a variety of different [StackExchange](https://stackexchange.com/) sites\n- A **beautiful command-line interface _for humans_**\n- A decently documented API\n- An optional **asynchronous API**\n- Decently easy-to-read code (formatted with [Black](https://github.com/psf/black))\n- And **open source code on [GitHub](https://github.com/ThatXliner/stacksearch/tree/Stable)**\n\n## Downsides 👎\n\n- Possibly _slower_ than the other modules\n- **The first PyPi project ever made by ThatXliner**\n- Not _fully_ (completely) optimized (well, after all, it\'s python)\n- ~~A big list of dependencies~~ (shortened in version 1.0.0 or so)\n\n## Current Features 😁\n\n- **Everything listed in the \'Benefits\' section of the README above**\n- Mostly, **if not fully**, [type-hinted](https://www.python.org/dev/peps/pep-0585/)\n- A **beautiful, simple, yet powerful command-line interface** (via [argparse](https://docs.python.org/3/library/argparse.html) and [blessings](https://pypi.org/project/blessings/))\n- **Asynchronous** StackOverflow requests!\n- The ability to **crank out raw [JSON](https://www.json.org/json-en.html) data** to **_use_**\n- And an **API**\n\n## Future Features 🏃\u200d♂️\n\n- [x] ~~Asynchronous StackOverflow requests!~~ (Done in v1.1.0)\n- [x] [Documentation](https://stacksearch.readthedocs.io/en/latest/) (_Sort of_ added in v1.2.8)\n- [ ] Object-oriented APIs\n- [ ] Python backwards-compatibility (3.6 to 3.9)\n- [ ] Being able to scrape _all_ StackOverflow sites/pages\n- [x] ~~A better README~~ (Done in v1.0.0.1)\n- [ ] Being able to output different formats of data (e.g. YAML, TOML, XML, etc)\n- [ ] And more command-line options\n\n## Usage Examples\n\n- For creating a text editor extension built on this package\n\n- For searching StackOverflow and/or **other StackExchange websites** without leaving the Terminal (for those [Vim](https://www.vim.org/) people)\n\n- For getting lots of answers from all StackExchange sites you know\n\n## License\n\nMIT License\n\n```text\nCopyright (c) 2020 ThatXliner\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n```\n\n## Code style guide 😳\n\n[Black](https://github.com/psf/black). We (I, right now.) use the black formatter to format our code. **It\'s pretty strict.**\n\nWe also use NumPy style docstrings.\n\n## Contributing ✏️\n\n![GitHub contributors](https://img.shields.io/github/contributors/ThatXliner/stacksearch)\n\nPlease feel free to contribute!\n\n## Links 📎\n\n[GitHub](https://github.com/ThatXliner/stacksearch/tree/Stable) (Possibly this page)\n\n[PyPi](https://pypi.org/project/stacksearch/) (Possibly this page)\n\n[Travis-CI](https://travis-ci.com/github/ThatXliner/stacksearch)\n',
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
