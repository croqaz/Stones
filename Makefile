.PHONY: clean lint coverage test

clean:
	rm -rf `find . -name __pycache__`
	rm -rf `find . -name .mypy_cache`
	rm -rf `find . -name .pytest_cache`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf coverage
	rm -rf build
	rm -rf cover

lint:
	python -m flake8p stones

coverage:
	python -m pytest --cov-report term --cov=stones/ tests/

test:
	python -m pytest -ra -sv tests/
