PYTHON := python3
PROJECT_NAME := stacksearch

test:
	@make deps
	@$(PYTHON) -m ensure pip && $(PYTHON) -m pip install pytest-cov pytest-asyncio pytest-random
	@pytest tests/ -vvv --durations=3 --cov=stacksearch
deps:
	@$(PYTHON) -m ensurepip
	@echo "Installing dependencies..."
	@$(PYTHON) -m pip install -r requirements.txt > /dev/null

dev-deps:
	@$(PYTHON) -m ensurepip
	@echo "Installing developer dependencies..."
	@$(PYTHON) -m pip install -r dev-requirements.txt > /dev/null

build:
	@$(PYTHON) setup.py sdist bdist_wheel

clean:
	@$(PYTHON) -m ensurepip
	@find . -type d \( -name '__pycache__' -or -name '*.egg-info' -or -name 'dist' -or -name 'build' -or -name '.pytest_cache' \)  -exec rm -rf {} +
	@black . || @$(PYTHON) -m pip install black > /dev/null || @echo "Black failed."
develop:
	@$(PYTHON) -m ensurepip
	@$(PYTHON) setup.py sdist bdist_wheel
	@$(PYTHON) -m pip install -e .
plush:
	@git pull --all
	@git push --all
sync:  # Made by (and for) ThatXliner
	@git checkout master && git merge Stable && make plush
	@git checkout preStable && git merge Stable && make plush
	@git checkout Stable
