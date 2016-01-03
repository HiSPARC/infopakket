.PHONY: all distclean clean gh-pages latexmk-recursive distclean-recursive clean-recursive index

TEXFILES=$(wildcard *.tex)
TARGETS=$(patsubst %.tex,%.pdf,$(TEXFILES))
TEX_DIRECTORIES=$(sort $(dir $(wildcard */*.tex)))
BRANCH=notebooks

# '-recursive' rules are based on a Makefile by Santiago Gonzalez Gancedo
# https://github.com/sangonz/latex_makefile
# which was a modified version of a Makefile by Johannes Ranke,
# which was based on Makesfiles by Tadeusz Pietraszek

all: latexmk-recursive
distclean: distclean-recursive
clean: clean-recursive

latexmk-recursive:
	for dir in $(TEX_DIRECTORIES); do \
		cd $$dir; \
		echo $$dir; \
		latexmk -shell-escape -quiet -pdf *.tex; \
		cd ..; \
	done

distclean-recursive:
	for dir in $(TEX_DIRECTORIES); do \
		cd $$dir; \
		latexmk -quiet -C *.tex; \
		cd ..; \
	done

clean-recursive:
	for dir in $(TEX_DIRECTORIES); do \
		cd $$dir; \
		latexmk -quiet -c *.tex; \
		cd ..; \
	done

index:
	python generate_index.py


# Add to allow only from master branch: ifeq ($(strip $(shell git branch --list | grep \*\ master | wc -l)), 1)

gh-pages:
ifeq ($(strip $(shell git status --porcelain | wc -l)), 0)
	git checkout gh-pages
	git rm -rf .
	git clean -dxf
	git checkout HEAD .nojekyll .gitignore
	git checkout $(BRANCH) -- generate_index.py index_template.html
	git checkout $(BRANCH) -- images styles
	git checkout $(BRANCH) -- style.tex style_brief.tex style_werkblad.tex common_style.tex HiSPARC_header.pdf
	git checkout $(BRANCH) -- Makefile
	git checkout $(BRANCH) -- $(TEX_DIRECTORIES)
	git checkout $(BRANCH) -- Notebooks
	$(MAKE) index
	# $(MAKE) all
	mkdir pdf
	# mv -fv */*.pdf pdf/
	mkdir notebooks
	mv -fv Notebooks/*.ipynb notebooks/
	rm -rf $(TEX_DIRECTORIES)
	rm -rf Notebooks
	rm -f generate_index.py index_template.html
	rm -f style.tex style_brief.tex style_werkblad.tex common_style.tex HiSPARC_header.pdf
	rm -f Makefile
	git add -A
	git commit -m "Generated gh-pages for `git log $(BRANCH) -1 --pretty=short --abbrev-commit`"
	git checkout $(BRANCH)
else
	$(error Working tree is not clean, please commit all changes.)
endif
