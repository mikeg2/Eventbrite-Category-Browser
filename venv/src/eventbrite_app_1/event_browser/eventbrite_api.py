import requests
import ConfigParser
from urllib.parse import urlparse

EB_API_CONFIG_URL = './event_browser.cfg'
config = ConfigParser.ConfigParser().readfp(open(EB_API_CONFIG_URL))['eventbrite']

#--- General Fetching ---

def fetch(truncated_url):
    full_url = full_url(truncated_url)
    return request_json(full_url)

def full_url(truncated_url):
    token = config['eventbrite_api_token']
    base_url = config['eventbrite_base_url']
    complete_url = urlparse.urljoin(base_url, truncated_url)
    full_url = add_params(complete_url, {'token': token})
    return full_url

def add_params(url, params):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)

def request_json(url):
    r = requests.get(url)
    if r.status_code != 200: # check if this should be more inclusive
        raise FailedApiRequest('Failed Eventbrite Api Request', url, r.status_code)
    return r.json()

#TODO: Add flash for errors
class FailedApiRequest(Exception):
    def __init__(self, message, url, status_code):
        super(FailedApiRequest, Exception).__init__(message)
        self.url = url
        self.status_code = status_code


#--- Specific Requests ---

def fetch_categories(page_number=1):
    trunc_url = config['categories_truncated_url']
    return fetch(trunc_url, {
            page: page_number
        }).categories

def fetch_events_by_category(categories, page_number=1, range_end_time=None):
    search_url = config['event_search_truncated_url']
    return fetch(search_url, {
        'categories': ','.join(categories),
        'page': page_number,
        'range_end': range_end_time
    })


# -- util --

def create_fetch_shortcut(trunc_url):
    def shortcut():
        fetch(trunc_url)
    return shortcut