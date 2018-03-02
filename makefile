VENV_DIR = $(HOME)/.virtualenvs
VENV_NAME = ${VENV_DIR}/pyrencode
PYTHON_BIN_DIR = ${VENV_NAME}/bin
PYTHON = ${PYTHON_BIN_DIR}/python
PIP = ${PYTHON_BIN_DIR}/pip

.PHONY: venv dist install

venv:
	mkdir -p ${VENV_DIR}
	virtualenv ${VENV_NAME}

dist:
	${PYTHON} setup.py sdist bdist_wheel

install:
	${PIP} install -e .
