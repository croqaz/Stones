
ENV=./env/bin

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +

update:
	${ENV}/pip install -U -r requirements.txt

lint:
	${ENV}/flake8 stones

coverage:
	${ENV}/pytest --cov-report term --cov=stones tests/

test:
	${ENV}/pytest -ra --capture=no --verbose tests/

icky:
	${ENV}/python -m sticky.cli -s stones/
