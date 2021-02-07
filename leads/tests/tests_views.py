from django.test import TestCase
from django.shortcuts import reverse
import requests
# Create your tests here.

class LandingpageTest(TestCase):
    def test_status_code(self):
        response=self.client.get(reverse("landing-page"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"landing.html")
        print(response.status_code)

'''    def test_template_name(self):
        pass'''