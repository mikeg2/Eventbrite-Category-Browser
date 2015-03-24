from django.test import TestCase

# Ideally would use dummy data for these tests instead of real Eventbrite data
# But no way to decouple views.py from eventbrite_api.py without adding a lot of unnecessary boilerplate

class EventBrowserViewTests(TestCase):
    def test_category_no_param_page(self):
        response = self.client.get('/')
        self.assert_categories_page(response)
        self.assertNotContains(response, 'events-wrapper')

    def test_category_with_events_page(self):
        response = self.client.get('/?cat=101&cat=103&cat=105')
        self.assert_categories_page(response)
        self.assertContains(response, 'events-wrapper')

    def test_categories_with_events_and_req_time_page(self):
        response = self.client.get('/?req_time=2015-03-24T00:48:23Z&page=1&cat=199&cat=199&cat=199')
        self.assert_categories_page(response)
        self.assertContains(response, 'events-wrapper')
        self.assertContains(response, 'Insomnia Gaming Festival')
        self.assertContains(response, 'Next')
        self.assertNotContains(response, 'Previous')

    def test_categories_pagnation(self):
        PAGE_NUM = '4'
        response = self.client.get('/?req_time=2015-03-21T00:11:21Z&cat=119&cat=199&cat=107&page=' + PAGE_NUM)
        self.assertContains(response, 'Page ' + PAGE_NUM)
        # Can't test contents since depends on outside API. No clear way to fix issue

    def assert_categories_page(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse_categories.html')
        self.assertNotContains(response, 'alert-danger')