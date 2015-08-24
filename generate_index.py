import glob
import os
import re
from operator import itemgetter
from collections import OrderedDict

import jinja2


PATH = os.path.dirname(__file__)


def make_index(infopakket):
    template_path = os.path.join(PATH, 'index_template.html')
    with open(template_path) as template_file:
        template = template_file.read()
    template = jinja2.Template(template)
    index = template.render(infopakket=infopakket)
    index_path = os.path.join(PATH, 'index.html')
    with open(index_path, 'w') as index_file:
        index_file.write(index)


def get_categories():
    """Read the categories from the common_style file

    The order of the categories is preserved.

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

    infopakket = OrderedDict((category, {'title': title, 'documents': []})
                             for category, title in categories)

    for path in glob.glob(os.path.join(PATH, '*/*.tex')):
        if 'examples' in path:
            continue
        filename = os.path.splitext(os.path.basename(path))[0] + '.pdf'
        document = {'filename': filename}
        try:
            document['title'] = fix_title(find_first(title_finder, path)[0])
            document['version'] = find_first(version_finder, path)[0]
            category, document['rank'] = find_first(cat_rank_finder, path)
        except Exception:
            print 'Failed for: ', path
            pass
        else:
            infopakket[category]['documents'].append(document)

    for key in infopakket.keys():
        infopakket[key]['documents'].sort(key=itemgetter('rank'))
    return infopakket


def fix_title(title):
    title = title.replace(r'\hisparc', 'HiSPARC')
    title = title.replace(r'\pmt', 'PMT')
    title = title.replace(r'\gps', 'GPS')
    title = title.replace(r'\adc', 'ADC')
    return title.decode('utf-8').encode('ascii', 'xmlcharrefreplace')


def find_first(finder, path):
    for line in open(path):
        result = finder.search(line)
        if result:
            return result.groups()
    raise Exception


if __name__ == "__main__":
    categories = get_categories()
    infopakket = get_documents(categories)
    make_index(infopakket)
