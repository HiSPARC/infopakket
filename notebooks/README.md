# Notebooks for HiSPARC

Notebooks are stored in git in markdown format using `notedown`: https://github.com/aaren/notedown

Markdown diffs are human-readable.

## Conversion to markdown

Convert a notebook into markdown, stripping all outputs:

```
notedown input.ipynb --to markdown --strip > output.md
```

## Conversion to ipynb

This needs to be included in `make github-pages`:
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
c.NotebookApp.contents_manager_class = 'notedown.NotedownContentsManager'
```

## JSON output in commits

When saving a markdown notebook in Jupyter, output is saved in JSON blocks. A PR for automatic stripping/conversion during save exists:https://github.com/aaren/notedown/issues/44
For now, we need to save without output and optionally strip JSON from markdown:

```
notedown with_output_cells.md --to markdown --strip > no_output_cells.md
```
