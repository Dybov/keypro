"""
Module: interactive_points.tests

This module contains the tests for the interactive_points app
"""

from django.test import TestCase
from django.urls import reverse


class IndexViewTests(TestCase):
    """Tests for the .views.index"""

    def test_index_page_works(self):
        """Test that the index page works correctly."""
        response = self.client.get(reverse("interactive_points:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="map"')
