
ENV=./env/bin

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +

clean-build:
	rm -f .coverage
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

update:
	${ENV}/pip install -U -r requirements.txt

lint:
	${ENV}/flake8 graphh

tests:
	${ENV}/pytest -ra -s -v test/
