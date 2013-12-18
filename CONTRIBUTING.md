How to contribute
=================

All documents are writen in LaTeX. This file provides LaTeX code
examples to demonstrate proper code style. Using a consistent style
makes it easier for other to read and understand the source files.


Preamble
--------

Start with importing the general style and defining the document title,
author. Then choose a category (e.g. `\docanalyse`), with a sequence
number and a two letter document code. And finally a version number.
Then beging the document by creating the title page.

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

Namen als \hisparc en \jsparc zien er anders uit de de rest van de tekst.
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
