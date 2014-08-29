# -*- coding: utf-8 -*-
import logging
from settings import jinja_env
from math import ceil
import urlparse
import urllib
#from sphinxsearch import SphinxClient, SPH_MATCH_EXTENDED

PER_PAGE = 21

def get_list(db_model, page_num, filter_dict={}):
    "Возращает отпагинированный список для модели db_model и страницы page_num"
    cursor = db_model.get_id_cursor(filter_dict)
    page = int(page_num) - 1
    logging.debug(u'Выбрано из БД: %s - %s' % (page * PER_PAGE, page * PER_PAGE + PER_PAGE))
    items = [db_model.get_middle(x.id) for x in cursor.skip(page * PER_PAGE).limit(PER_PAGE)]
    return items

def get_list_all(db_model, filter_dict={}):
    "Возращает отпагинированный список для модели db_model и страницы page_num"
    items = [db_model.get_middle(x.id) for x in db_model.get_id_cursor(filter_dict)]
    return items

class Pagination(object):
    def __init__(self, page, total_count, per_page=PER_PAGE):
        self.page = page
        if self.page <= 0:
            self.page = 1
        self.total_count = total_count
        self.per_page = per_page
        self.pages = int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


def update_querystring(url, **kwargs):
    base_url = urlparse.urlsplit(url)
    query_args = urlparse.parse_qs(base_url.query)
    query_args.update(kwargs)

    for arg_name, arg_value in query_args.iteritems():
        if arg_value is None:
            if query_args.has_key(arg_name):
                del query_args[arg_name]
        else:
            if type(arg_value) == list:
                arg_value = arg_value[0]
            try:
                query_args[arg_name] = arg_value.encode('utf-8')
            except:
                query_args[arg_name] = arg_value

    query_string = urllib.urlencode(query_args)
    return urlparse.urlunsplit((base_url.scheme, base_url.netloc,
        base_url.path, query_string, base_url.fragment))
jinja_env.globals['update_querystring'] = update_querystring

def url_for_other_page(uri, page):
    return update_querystring(uri, page=page)
jinja_env.globals['url_for_other_page'] = url_for_other_page


def filter_list(module, page, filter):
    items = get_list(module, page, filter)
    count_all = module.get_count(filter)
    return {
        'items': items,
        'count_all': module.get_count(filter),
        'count': len(items),
        'pagination': Pagination(page, count_all),
    }

"""
def search(query, module):
    sc = SphinxClient()
    sc.SetMatchMode(SPH_MATCH_EXTENDED)
    found = sc.Query(query.encode('utf-8'), module.get_db_name())

    result = []
    if found:
        for match in found["matches"]:
            result.append(match["id"])

    return result

jinja_env.globals['date'] = date_for_template
jinja_env.globals['datetime'] = datetime_for_template
"""