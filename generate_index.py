import re

from operator import itemgetter
from pathlib import Path

import jinja2

PATH = Path(__file__).parent


def make_index(infopakket, notebooks):
    template_path = PATH / 'index_template.html'
    template = jinja2.Template(template_path.read_text())
    index = template.render(infopakket=infopakket, notebooks=notebooks)
    index_path = PATH / 'index.html'
    index_path.write_text(index)


def get_categories():
    """Read the categories from the common_style file

    :return: list of tuples which contain the shortname and the title name
             for each category.

    """
    finder = re.compile(r'\\doc(.*?)\}.*\{(.*?)\}\{#1')
    path = PATH / 'style_common.tex'
    categories = []
    for line in open(path):
        result = finder.search(line)
        if result:
            categories.append(result.groups())
    return categories


def get_documents(categories):
    """Find documents for a specific category

    :param categories: list of categories
    :return: list of tuples which contain the shortname and the title name
             for each category.

    """
    title_finder = re.compile(r'\\title\{(.*)\}')
    version_finder = re.compile(r'\\version\{(.*)\}')
    cat_rank_finder = re.compile(r'\\doc(.*?)\{([0-9]+)\}')

    infopakket = {
        category: {'title': title, 'documents': []}
        for category, title in categories
    }

    for path in PATH.glob('*/*.tex'):
        if 'examples' in path.parts:
            continue
        filename = path.with_suffix('.pdf').name
        document = {'filename': filename}
        contents = path.read_text()
        try:
            document['title'] = fix_title(title_finder.search(contents).group(1))
            document['version'] = version_finder.search(contents).group(1)
            category, document['rank'] = cat_rank_finder.search(contents).groups()
        except AttributeError:
            if 'uitwerkingen' in filename:
                contents = Path(str(path).replace('_uitwerkingen', '')).read_text()
                document['title'] = fix_title(title_finder.search(contents).group(1))
                document['version'] = version_finder.search(contents).group(1)
                _, document['rank'] = cat_rank_finder.search(contents).groups()
                category = 'docent'
            else:
                raise
        infopakket[category]['documents'].append(document)

    for value in infopakket.values():
        value['documents'].sort(key=itemgetter('rank'))

    return infopakket


def fix_title(title):
    title = (
        title
        .replace(r'\hisparc', 'HiSPARC')
        .replace(r'\pmt', 'PMT')
        .replace(r'\gps', 'GPS')
        .replace(r'\adc', 'ADC')
    )
    return title.encode('ascii', 'xmlcharrefreplace').decode('utf-8')


def get_notebooks():
    """Retrieve all notebooks from the directory tree."""

    notebooks = [
        {
            'filename': filename.with_suffix('.ipynb'),
            'title': make_notebook_title(filename),
        }
        for filename in PATH.glob('notebooks/*.md')
    ]
    return notebooks


def make_notebook_title(filename):
    """Make a title out of the notebook filename.

    Remove the extension, remove the prefix, replace underscores by spaces.

    """

    return filename.stem.partition('_')[2].replace('_', ' ')


if __name__ == "__main__":
    categories = get_categories()
    infopakket = get_documents(categories)
    notebooks = get_notebooks()
    make_index(infopakket, notebooks)
