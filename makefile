test:
	python3 -m pytest

coverage:
	python3 -m pytest --cov=monitor tests

.PHONY: test coverage
