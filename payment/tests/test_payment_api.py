from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from library.models import Book
from borrowing.models import Borrowing
from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentDetailSerializer

PAYMENT_URL = reverse("payment:payment-list")


def sample_book(**params):
    defaults = {
        "title": "Sample book",
        "author": "Sample author",
        "cover": "HARD",
        "inventory": 5,
        "daily_fee": 12.99,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def sample_borrowing(**params):
    defaults = {
        "expected_return_date": datetime.now().date() + timedelta(days=1),
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)


def sample_payment(**params):
    defaults = {
        "payment_status": "PENDING",
        "payment_type": "PAID",
        "money_to_pay": 20.30,
    }
    defaults.update(params)

    return Payment.objects.create(**defaults)


def detail_url(payment_id):
    return reverse("payment:payment-detail", args=[payment_id])


class UnauthenticatedPaymentApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PAYMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPaymentApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@gmail.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_list_of_user_payments(self):
        second_user = get_user_model().objects.create_user(
            "user2@gmail.com", "password2"
        )

        borrowing1 = sample_borrowing(user=self.user, book=sample_book())
        borrowing2 = sample_borrowing(
            user=second_user, book=sample_book(title="Second book")
        )
        sample_payment(borrowing=borrowing1)
        sample_payment(borrowing=borrowing2)

        res = self.client.get(PAYMENT_URL)
        payments = Payment.objects.filter(borrowing__user=self.user)
        serializer = PaymentSerializer(payments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_payment_detail(self):
        borrowing = sample_borrowing(user=self.user, book=sample_book())
        payment = sample_payment(borrowing=borrowing)

        url = detail_url(payment.id)
        res = self.client.get(url)

        serializer = PaymentDetailSerializer(payment)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AdminPaymentApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@gmail.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_list_of_all_payments(self):
        user = get_user_model().objects.create_user(
            "user@gmail.com", "password2"
        )

        admin_borrowing = sample_borrowing(
            user=self.user, book=sample_book(title="Admin book")
        )
        user_borrowing = sample_borrowing(
            user=user, book=sample_book(title="User book")
        )
        sample_payment(borrowing=admin_borrowing)
        sample_payment(borrowing=user_borrowing)

        res = self.client.get(PAYMENT_URL)
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
