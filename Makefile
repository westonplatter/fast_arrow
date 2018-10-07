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
