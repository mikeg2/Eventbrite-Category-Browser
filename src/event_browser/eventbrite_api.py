import requests
from cachecontrol import CacheControl
import urlparse
import urllib
from eventbrite_app_1.settings import BASE_DIR
from configobj import ConfigObj
from django.core.cache import cache
import os

BROWSER_VIEW_CONFIG_URL = os.path.join(BASE_DIR, 'event_browser/event_browser.cfg')
config = ConfigObj(BROWSER_VIEW_CONFIG_URL)['eventbrite']

#--- General Fetching ---

def fetch(truncated_url, opt={}):
    api_full_url = full_url(truncated_url)
    return get_json(api_full_url, opt)

# inj parameter added to allow for testing
def full_url(truncated_url, inj=config):
    token = inj['eventbrite_api_token']
    base_url = inj['eventbrite_base_url']
    complete_url = urlparse.urljoin(base_url, truncated_url)
    result_full_url = add_params(complete_url, {'token': token})
    return result_full_url

# Adapted from example here: http://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python
def add_params(url, params):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)

def get_json(api_full_url, opt):
    perm_cache = opt.get('perm_cache', False)
    cache_key = get_request_key(api_full_url)
    if perm_cache:
        result = cache.get(cache_key)
        if result:
            return result
    result = request_json(api_full_url, opt)
    if perm_cache:
        cache.set(cache_key, result)
    return result

# Not intelligent enough to recognize for get params in different orders
def get_request_key(url):
    return 'get ' + url

def request_json(url, opt={}):
    params = opt.get('params', {})
    result = requests.get(url, params=params)
    if is_error_code(result.status_code):
        raise FailedApiRequest('Eventbrite API returned error', url, result.status_code)
    return result.json()

def is_error_code(status_code):
    return int(status_code) >= 400

class FailedApiRequest(Exception):
    def __init__(self, message, url, status_code):
        super(FailedApiRequest, self).__init__(message)
        self.url = url
        self.status_code = status_code


#--- Specific Requests ---

def fetch_categories(page_number=1, cached=False):
    trunc_url = config['categories_truncated_url']
    return fetch(trunc_url, {
            'params': {
                'page': page_number
            },
            'perm_cache': cached
        })

# Though all category results fit in one request page as of 3/21/2015,
# the code should work even if category results are many pages long
# 
# WARNING: Untested for results more than one page long
def fetch_all_categories(cached=False):
    all_cat = []
    page = 1
    while True:
        cat_data = fetch_categories(page, cached)
        categories = cat_data['categories']
        all_cat += categories
        pagination = cat_data['pagination']
        if pagination['page_count'] == page:
            break
        page += 1
    return all_cat

def fetch_events_by_category(categories, page_number=1, range_end_time=None):
    search_url = config['event_search_truncated_url']
    str_categories = [str(cat) for cat in categories]
    return fetch(search_url, {
        'params': {
            'categories': ','.join(str_categories),
            'page': page_number,
            'date_modified.range_end': range_end_time
        }
    })