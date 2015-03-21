import unittest
from eventbrite_api import *
import datetime
import requests
from cachecontrol import CacheControl

# Could try to decouple eventbrite_api.py from the actual request object, therefor making unit tests independent of the API
# However, that also reduces the tests' usefullness (though also reduces the time they take)

class TestFetchFunctions(unittest.TestCase):

    def setUp(self):
        pass

    # does not test pagnation, since categories can't paginate as of 3/17/2015
    def test_fetch_categories(self):
        categories_data = fetch_categories()
        categories = categories_data['categories']
        pagination = categories_data['pagination']
        assert pagination['page_number'] == 1
        self.assert_pagination(categories, pagination)
        self.assert_categories(categories)

    def test_fetch_all_categories(self):
        all_cat = fetch_all_categories()
        self.assert_categories(all_cat)

    def test_fetch_all_categories_cached(self):
        all_cat = fetch_all_categories(True)
        self.assert_categories(all_cat)
        all_cat = fetch_all_categories(True)
        self.assert_categories(all_cat)

    def assert_categories(self, categories):
        for cat in categories:
            assert cat['id']
            assert cat['resource_uri']
            assert cat['name']
            assert cat['name_localized']
            assert cat['short_name']
            assert cat['short_name_localized']

    def assert_pagination(data, pagination):
        assert len(data) <= pagination['page_size']
        assert len(data) > 0

    def test_get_request_obj(self):
        assert get_request_obj() is requests
        assert get_request_obj({'cached': False}) is requests
        assert type(get_request_obj({'cached': True})) is requests.sessions.Session

    def test_get_cached_requests(self):
        assert type(get_cached_requests()) is requests.sessions.Session
        assert get_cached_requests() is get_cached_requests()

    def test_full_url(self):
        inj = {
            'eventbrite_base_url': 'https://test.com/v1/',
            'eventbrite_api_token': '1'
        }
        cases_and_results = [
            ('/categories', 'https://test.com/categories?token=1'),
            ('category', 'https://test.com/v1/category?token=1'),
            ('event', 'https://test.com/v1/event?token=1'),
            ('event/search', 'https://test.com/v1/event/search?token=1'),
            ('/event/search/', 'https://test.com/event/search/?token=1'),
        ]
        for case, expected in cases_and_results:
            assert expected == full_url(case, inj)

    def test_add_params(self):
        cases_and_results = [
            (('test.com', {'var1': 1}), 'test.com?var1=1'),
            (('https://test.com', {'var2': 3, 'var3': 7}), 'https://test.com?var3=7&var2=3'),
            (('', {}), ''),
            (('', {'var 1': 1}), '?var+1=1'),
        ]
        for case, expected in cases_and_results:
            print(case, expected)
            assert expected == add_params(case[0], case[1])

    def test_request_json_no_params(self):
        json_test_url = 'http://ip.jsontest.com/'
        result = request_json(json_test_url)
        assert result['ip']

    #TODO: need to test request_json with params

    def test_fetch_events_by_category(self):
        test_cat = [101, 102, 103]
        data = fetch_events_by_category(test_cat)
        events = data['events']
        pagination = data['pagination']
        assert len(events) > 0 # reasonable assumption
        self.assert_pagination(events, pagination)
        for e in events: # tests the fields that the rest of the program expects to be filled out
            assert e['name']
            assert e['url']
            assert e['category_id'] in test_cat