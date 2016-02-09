HiSPARC infopakket
==================

Dit zijn documenten met lesmateriaal en praktische opdrachten gericht op
middelbare scholen. Het doel van het materiaal is om docenten en
leerlingen een ingang te bieden voor onderhoud en onderzoek. Hiervoor
zijn een aantal opdrachten samengesteld die de docent voor zijn lessen
kan gebruiken. Door deze opdrachten uit te voeren ervaren leerlingen de
verschillende facetten van wetenschappelijk onderzoek:

- Het onderhouden van een experimentele opstelling.
- Het opvragen en verwerken van de digitaal opgeslagen meetgegevens.
- Op basis van de meetgegevens de onderzoeksvraag beantwoorden. 


HiSPARC infopackage
-------------------

These are documents containing course material and practical assignments
for Dutch high schools. The purpose is to give teachers and students easy
entry into learning maintenance and doing research. To accomplish this,
several assignments have been created which the teacher can use in his
courses. By using these the students learn the different facets of
scientific research:

- Maintaining a experimental setup.
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

First ensure that the `gh-pages` branch is up-to-date. Then go back to
the `master` branch. To publish new documents or changes run the
terminal command `make gh-pages` from the root repository directory
while in the `master` branch. This will first checkout the `gh-pages`
branch. Then get all directories containing a tex file from the `master`
branch, and `index.html`, `styles` and `images`. It will then build all
pdf files, which will be copied to a `pdf` directory, after which the
source directories will be removed. Then a new commit will automatically
be created. And the `master` branch will be checked out again. Once you
push the `gh-pages` branch to GitHub, the changes will be available
online.
