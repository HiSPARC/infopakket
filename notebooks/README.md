# Notebooks for HiSPARC

[![Binder](http://mybinder.org/badge.svg)](http://mybinder.org/v2/gh/HiSPARC/infopakket/gh-pages?filepath=notebooks)

Notebooks are stored in git in markdown format using `notedown`: https://github.com/aaren/notedown


## Conversion to markdown

Convert a notebook into markdown, stripping all outputs:

```
notedown input.ipynb --to markdown --strip > output.md
```


## Conversion to ipynb

This needs to be included in `make` for github-pages:
```
notedown input.md > output.ipynb
```


## Markdown in Jupyter:

You can configure Jupyter to seamlessly use markdown as its storage format.
```
jupyter notebook --generate-config
```

Add the following to `.jupyter/jupyter_notebook_config.py`
```
c.NotebookApp.contents_manager_class = 'notedown.NotedownContentsManagerStripped'
```
