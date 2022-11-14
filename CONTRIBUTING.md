How to contribute
=================

All documents are written in LaTeX. This file provides LaTeX code
examples to demonstrate proper code style. Using a consistent style
makes it easier for other to read and understand the source files.

To submit new documents or suggest changes to existing ones you can
create create a Pull Request or Issue on GitHub. If you do not have a
GitHub account you can send documents (preferably as .tex, other
document types are allowed for the initial submit) to info@hisparc.nl.


Repository structure
====================

Work in progress
----------------

It is best to keep a work in progress (a new document not yet ready to
be 'published') in a separate branch from `master`. This ensures that it
is not accidentally published. Once you believe it is ready, create a
pull request to ask someone to review it. Once reviewed and corrected it
can be merged to `master`.


Completed documents
-------------------

Once a document is completed (version 1.0) it should appear in the `master`
branch and be added to the `index.html`.


Directory structure
===================

The main directory contains the common files; the style, HiSPARC logo,
gh-pages files. Each document is inside a directory with a recognisable
lowercase and underscored name (e.g. `richting_reconstructie`). Inside
each of those is the .tex file and a directory called Figures which
contains all figures used in the document.


Document structure
==================


Preamble
--------

Start with importing the general style and defining the document title,
author. Then choose a category (e.g. `\docanalyse`), with a sequence
number and a two letter document code. And finally a version number.
Then begin the document by creating the title page.

```latex
\input{../style}

\title{Voorbeeldje}
\author{A. de Laat}
\docanalyse{3}{VB}
\version{1.0}

\begin{document}

\maketitle
```


Sections
--------

Start each new section with a `\section{}`. For common terms use the
shortcuts to ensure proper capitalisation and emphasis, supported terms
can be found in the `style.tex`. When writing values with units use the
`\SI{}{}` command, where the first argument is the value and the second
the units. Here are some examples:

```latex
\section{Begin}

Namen als \hisparc en \jsparc zien er anders uit dan de rest van de tekst.
Ook getallen met eenheden, zoals \SI{120.3}{\micro\meter} hebben speciale
commando's, zo kan later eenvoudig de weergave aangepast worden. En dit
is allemaal terug te lezen in \cite{tekst}.
```


Bibliography
------------

Add all reference to the bibliography at the end of the document

```latex
\begin{thebibliography}{9}
    \bibitem{tekst}
        Door N.G. Schultheiss, \emph{Botsen en Lenzen}, CC-BY-SA-3.0, via \hisparc
\end{thebibliography}

\end{document}
```


Text width
----------

Try to keep lines shorter than 72 characters, this makes it easier to
track changes and works better for some text editors.
