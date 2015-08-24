import glob
import os
import re
from operator import itemgetter

import jinja2


PATH = os.path.dirname(__file__)


def make_index(documents):
    pass


def get_categories():
    """Read the categories from the common_style file

    The order fo the categories is preserved.

    :return: list of tuples which contain the shortname and the title name
             for each category.

    """
    finder = re.compile(r'doc(.*?)\}.*\{(.*?)\}\{#1')
    path = os.path.join(PATH, 'common_style.tex')
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
    cat_rank_finder = re.compile(r'\\doc(.*?)\{([0-9]+)\}')
    version_finder = re.compile(r'\\version\{(.*)\}')

    documents = {category: [] for category, title in categories}

    for path in glob.glob(os.path.join(PATH, '*/*.tex')):
        filename = os.path.splitext(os.path.basename(path))[0] + '.pdf'
        document = {'filename': filename}
        try:
            document['title'] = find_first(title_finder, path)[0]
            document['version'] = find_first(version_finder, path)[0]
            category, document['rank'] = find_first(cat_rank_finder, path)
        except Exception:
            print 'Failed for: ', path
            pass
        else:
            documents[category].append(document)

    for key in documents.keys():
        documents[key].sort(key=itemgetter('rank'))
    return documents


def find_first(finder, path):
    for line in open(path):
        result = finder.search(line)
        if result:
            return result.groups()
    raise Exception


if __name__ == "__main__":
    categories = get_categories()
    documents = get_documents(categories)
    make_index(documents)
