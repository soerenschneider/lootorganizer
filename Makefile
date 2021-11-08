tests: venv
	PYTHONPATH=lootorganizer venv/bin/python3 -m unittest lootorganizer/test_*.py

.PHONY: integrationtests
integrationtests: 
	venv/bin/python3 -m unittest inttest/itest_*.py

venv-test: venv
	if [ -f requirements-test.txt ]; then venv/bin/pip3 install -r requirements-test.txt; fi

lint:
	PYTHONPATH=lootorganizer venv/bin/pylint --output-format=text lootorganizer/

.PHONY: venv
venv:
	if [ ! -d "venv" ]; then python3 -m venv venv; fi
	venv/bin/pip3 install -r requirements.txt

install:
	sh install.sh
