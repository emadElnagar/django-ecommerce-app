from django.test import TestCase

# Create your tests here.

class HomePage(TestCase):
    def test_Homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
