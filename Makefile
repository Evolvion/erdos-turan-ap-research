VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
all: reproduce
venv:
	python -m venv $(VENV)
install: venv
	$(PIP) install -r requirements.txt
reproduce:
	$(PY) -m etap.cli engine --window 2048 --k 3 --sigma 0.2 --Cr 2
paper:
	lualatex paper/preprint.tex
test:
	$(PY) -m etap.cli selftest
