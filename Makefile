# Build pdfs for the TeX files

# '-recursive' rules are based on a Makefile by Santiago Gonzalez Gancedo
# which was a modified version of a Makefile by Johannes Ranke,
# which was based on Makesfiles by Tadeusz Pietraszek

TEXFILES=$(wildcard *.tex)
TARGETS=$(patsubst %.tex,%.pdf,$(TEXFILES))
TEX_DIRECTORIES=$(sort $(dir $(wildcard */*.tex)))

.PHONY: all
all: latexmk-recursive
.PHONY: distclean
distclean: distclean-recursive
.PHONY: clean
clean: clean-recursive

.PHONY: latexmk-recursive
latexmk-recursive:
	for dir in $(TEX_DIRECTORIES); do \
		echo '******** starting latexmk ********'; \
		cd $$dir; \
		echo $$dir; \
		latexmk -shell-escape -quiet -pdf *.tex || exit 1; \
		echo '******** finished latexmk ********'; \
		cd ..; \
	done

.PHONY: distclean-recursive
distclean-recursive:
	for dir in $(TEX_DIRECTORIES); do \
		cd $$dir; \
		latexmk -quiet -C *.tex; \
		cd ..; \
	done

.PHONY: clean-recursive
clean-recursive:
	for dir in $(TEX_DIRECTORIES); do \
		cd $$dir; \
		latexmk -quiet -c *.tex; \
		cd ..; \
	done

.PHONY: index
index:
	python generate_index.py

# Convert notebooks from markdown to ipynb

NOTEBOOKDIR=notebooks
NOTEBOOKSRCS:=$(wildcard $(NOTEBOOKDIR)/*.md)
NOTEBOOKSRCS:=$(filter-out $(NOTEBOOKDIR)/README.md, $(NOTEBOOKSRCS))
NOTEBOOKS:=$(NOTEBOOKSRCS:.md=.ipynb)

%.ipynb:%.md
	jupytext $<

.PHONY: notebooks
notebooks: $(NOTEBOOKS)
	@echo 'converted notebooks from .md to .ipynb'
