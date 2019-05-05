from django.test import TestCase
from django.urls import reverse


class ViewIndexTests(TestCase):
    def test_index_response(self):
        """
        Simple test which checks that the landing page response is 200
        """
        response = self.client.get(reverse('pages:index'))
        self.assertEqual(response.status_code, 200)
