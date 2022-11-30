from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

PAYMENT_URL = reverse("payment:payment-list")


class UnauthenticatedPaymentApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PAYMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
