# Notebooks for HiSPARC

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/HiSPARC/infopakket/gh-pages?filepath=notebooks)

Notebooks are stored in git in markdown format using `jupytext`: https://jupytext.readthedocs.io


## Install dependencies

Install the Jupytext package (use a virtual environment):

```
pip install jupytext
```

## Conversion to markdown

Convert a notebook into markdown, stripping all outputs:

```
jupytext input.ipynb --to markdown
```


## Conversion to ipynb

This needs to be included in `make` for github-pages:
```
jupytext input.md --to ipynb
```


## Automatic conversion in Jupyter

Consult the Jupytext Installation documentation for instructions to setup
automatic conversion to markdown.
