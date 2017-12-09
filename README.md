HiSPARC infopakket
==================

![http://img.shields.io/travis/HiSPARC/infopakket/master.svg](https://travis-ci.org/HiSPARC/infopakket)

Dit zijn documenten met lesmateriaal en praktische opdrachten gericht op
middelbare scholen. Het doel van het materiaal is om docenten en
leerlingen een ingang te bieden voor onderhoud en onderzoek. Hiervoor
zijn een aantal opdrachten samengesteld die de docent voor zijn lessen
kan gebruiken. Door deze opdrachten uit te voeren ervaren leerlingen de
verschillende facetten van wetenschappelijk onderzoek:

- Het onderhouden van een experimentele opstelling.
- Het opvragen en verwerken van de digitaal opgeslagen meetgegevens.
- Op basis van de meetgegevens de onderzoeksvraag beantwoorden. 

De documenten zijn te vinden op http://docs.hisparc.nl/infopakket/


HiSPARC infopackage
-------------------

These are documents containing course material and practical assignments
for Dutch high schools. The purpose is to give teachers and students easy
entry into learning maintenance and doing research. To accomplish this,
several assignments have been created which the teacher can use in his
courses. By using these the students learn the different facets of
scientific research:

- Maintaining an experimental setup.
- Requesting and processing the measurement data.
- Using the data to answer questions.


Generating pdfs
---------------

To create all pdf files for easier reading or printing, use the command
`make all`, this will build a pdf for each tex file in each
subdirectory. To clean up the extra files that are generated when
creating pdfs use `make clean`, to also remove the generated pdfs use
`make distclean`.


How to publish
--------------

Commits pushed to the master branch will be automatically build on Travis.
This means that all pdfs will be generated with LaTeX, the html index page
is rendered, and the IPython notebooks are converted from markdown to ipynb
files.

If this is all successful the result is pushed to the gh-pages branch
and made available via http://docs.hisparc.nl/infopakket/ .
