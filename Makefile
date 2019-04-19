.PHONY: test
test:
	pipenv run pytest

.PHONY: ci
ci:
	pipenv run pytest --cov=fast_arrow tests/

.PHONY: coveralls
coveralls:
	pipenv run coveralls

.PHONY: lint
lint:
	pipenv run tox -e lint

.PHONY: l
l:
	pipenv run flake8 --exclude fast_arrow/__init__.py,examples/*,setup.py


.PHONY: examples
examples:
	pipenv run run_all_examples
