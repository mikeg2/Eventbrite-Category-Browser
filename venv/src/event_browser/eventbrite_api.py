import requests
from cachecontrol import CacheControl
import urlparse
import urllib
from eventbrite_app_1.settings import BASE_DIR
from configobj import ConfigObj
import os

BROWSER_VIEW_CONFIG_URL = os.path.join(BASE_DIR, 'event_browser/event_browser.cfg')
config = ConfigObj(BROWSER_VIEW_CONFIG_URL)['eventbrite']

#--- General Fetching ---

def fetch(truncated_url, opt):
    api_full_url = full_url(truncated_url)
    return request_json(api_full_url, opt)

# inj parameter added to allow for testing
def full_url(truncated_url, inj=config):
    token = inj['eventbrite_api_token']
    base_url = inj['eventbrite_base_url']
    complete_url = urlparse.urljoin(base_url, truncated_url)
    result_full_url = add_params(complete_url, {'token': token})
    return result_full_url

def add_params(url, params):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)

def request_json(url, opt):
    request_obj = get_request_obj(opt)
    r = request_obj.get(url, params=opt.get('params', {}))
    if r.status_code != 200: # check if this should be more inclusive
        print("API CODE: ", r.status_code, " URL: ", url, "PARAMS: ", params, " OTHER: ", r.json())
        raise FailedApiRequest('Failed Eventbrite Api Request', url, r.status_code)
    return r.json()

def get_request_obj(opt):
    print("GET REQ OBJ: ", opt)
    if opt.get('cached', False):
        return get_cached_requests()
    else:
        return requests

def get_cached_requests():
    if get_cached_requests.cached_sess is None:
        sess = requests.session()
        cached_sess = CacheControl(sess)
        get_cached_requests.cached_sess = cached_sess
    return get_cached_requests.cached_sess
get_cached_requests.cached_sess = None
    

#TODO: Add flash for errors
class FailedApiRequest(Exception):
    def __init__(self, message, url, status_code):
        super(FailedApiRequest, self).__init__(message)
        self.url = url
        self.status_code = status_code


#--- Specific Requests ---

#TODO: Make it fetch all categories regardless of page size
def fetch_categories(page_number=1, cached=False):
    trunc_url = config['categories_truncated_url']
    return fetch(trunc_url, {
            'params': {
                'page': page_number
            },
            'cached': cached
        })

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


# -- util --

def create_fetch_shortcut(trunc_url):
    def shortcut():
        fetch(trunc_url)
    return shortcut