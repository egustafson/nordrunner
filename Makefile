# Makefile

PY_MODULES = nordrunner.py setup.py

.PHONY: lint flake8 test all install preflight

all: lint test
	python setup.py develop

lint:
	pylint ${PY_MODULES}

flake8:
	flake8 ${PY_MODULES}

test:
	pytest

preflight:
	pip install -r requirements.txt
	pip install -r requirements_dev.txt
