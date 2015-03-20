from django.test import TestCase

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
        response = self.client.get('/?req_time=2015-03-20T00%3A27%3A53Z&cat=119&cat=199&cat=107')
        self.assert_categories_page(response)
        self.assertContains(response, 'events-wrapper')
        self.assertContains(response, 'Insomnia Gaming Festival')
        self.assertContains('Next')
        self.assertNotContains('Previouse')

    def test_categories_pagnation(self):
        response = self.client.get('/?req_time=2015-03-20T00%3A27%3A53Z&page=4&cat=119&cat=199&cat=107')
        self.assertContains(response, 'Page 4 of')
        # Can't test contents since depends on outside API. No clear way to fix issue with dependency injection

    def assert_categories_page(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse_categories')