.PHONY: paper

VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
PYTHON ?= python3
all: reproduce
venv:
	$(PYTHON) -m venv $(VENV)
install: venv
	$(PIP) install -r requirements.txt
reproduce:
	PYTHONPATH=src $(PY) -m etap.cli engine --window 2048 --k 3 --sigma 0.2 --Cr 2
paper:
	lualatex paper/preprint.tex
test:
	PYTHONPATH=src $(PY) -m etap.cli selftest
