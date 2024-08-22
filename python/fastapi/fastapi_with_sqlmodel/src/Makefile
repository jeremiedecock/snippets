# Makefile with some convenient quick ways to do common things
# This file is mostly inspired by https://github.com/cta-observatory/ctapipe/blob/master/Makefile

include meta.make

###############################################################################

all: help

.PHONY : all \
         analyse \
         clean \
         cov \
         doc \
         doc-publish \
         doc-publish-github \
         doc-show \
         help \
         init \
         init-skeleton \
         list \
         pep8 \
         publish \
         test \
         trailing-spaces \


###############################################################################

PYTHON=python3

## HELP #######################################################################

#help:
#	@echo ''
#	@echo 'Available make targets:'
#	@echo ''
#	@echo '  help                Print this help message (the default)'
#	@echo '  init                Import submodules'
#	@echo '  clean               Remove generated files'
#	@echo '  develop             Make symlinks to this package in python install dir'
#	@echo '  test                Run tests'
#	@echo '  doc                 Generate Sphinx docs'
#	@echo '  doc-show            Generate and display docs in browser'
#	@echo '  analyze             Do a static code check and report errors'
#	@echo ''
#	@echo 'Advanced targets (for experts):'
#	@echo ''
#	@echo '  doc-publish-github  Generate and upload the docs to GitHub'
#	@echo ''

# See http://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile

help: list

list:
	@echo "Available targets:"
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs


###############################################################################

analyze:
	@pyflakes $(PYTHON_PACKAGE_NAME) examples

create-venv:
	conda deactivate
	rm -rf env
	python3 -m venv env
	source ./env/bin/activate
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt
	pip install -e .

activate-venv:
    conda deactivate
	source ./env/bin/activate

init:
	git submodule init
	git submodule update

cov:
	# See http://pytest-cov.readthedocs.io/en/latest/readme.html
	pytest --cov=$(PYTHON_PACKAGE_NAME) $(PYTHON_PACKAGE_NAME)/

doc:
	sphinx-build -b html docs/ build/sphinx/html/

doc-show:
	sphinx-build -b html docs/ build/sphinx/html/ --open-docs-in-browser

#doc-publish-github: doc
#	# See https://github.com/davisp/ghp-import
#	# Install: pip install ghp-import
#	ghp-import -n -p -m 'Update gh-pages docs' build/sphinx/html

#doc-publish-jdhp: doc
#	# AILIB_DOCS_URI is a shell environment variable that contains the
#	# destination URI of the HTML files.
#	@if test -z $$AILIB_DOCS_URI ; then exit 1 ; fi
#
#	# Upload the HTML files
#	rsync -r -v -e ssh $(HTML_TMP_DIR)/ ${AILIB_DOCS_URI}/

pep8:
	@pep8 --statistics

test:
	pytest

trailing-spaces:
	find $(PYTHON_PACKAGE_NAME) examples docs -name "*.py" -exec perl -pi -e 's/[ \t]*$$//' {} \;


## PUBLISH ####################################################################

#publish:


## CLEAN ######################################################################

init: clean

clean:
	@echo "Remove generated files"
	@rm -rvf docs/_build
	@rm -rvf build/
	@rm -rvf dist
	@rm -rvf sdist
	@rm -rvf *.egg-info/
	@rm -rvf htmlcov/
	@rm -rvf debian
	@rm -v MANIFEST
	@find . -type d -iname "__pycache__" -exec rm -rfv {} \;
	@find . -type f -iname "*.pyc" -exec rm -v {} \;
	@find . -type f -iname "*.pyo" -exec rm -v {} \;
	@find . -type f -iname "*.pyd" -exec rm -v {} \;
	@find . -type f -iname "*.so"  -exec rm -v {}
