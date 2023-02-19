from rest_framework import status
from rest_framework.test import APITestCase


class Categories(APITestCase):
    """Test-Categories"""

    def test_expected_fields(self):
        """test_expected_fields"""
        data = {"name": "IPhone"}
        response = self.client.post(data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SubCategories(APITestCase):
    """Test-SubCategories"""

    def test_expected_fields(self):
        """test_expected_fields"""
        data = {"name": "IPhone 14 Pro Max"}
        response = self.client.post(data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
