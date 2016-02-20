.PHONY: all install test clean

all: install

install:
	./setup.py install

test:
	tox

clean:
	./setup.py clean --all
	rm -rf *.egg-info/
	rm -rf .cache/
	rm -rf .eggs/
	rm -rf .tox/
	rm -rf dist/
	rm -f .coverage
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -delete
