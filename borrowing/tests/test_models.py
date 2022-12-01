import datetime

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from rest_framework.test import APIClient

from borrowing.models import Borrowing
from library.models import Book


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
    expected_return_date = datetime.date.today() + datetime.timedelta(days=3)
    defaults = {
        "expected_return_date": expected_return_date,
        "book": sample_book(),
        "user": params["user"]
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)


class ModelsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_expected_return_date_lte_borrow_date_forbidden(self):
        invalid_expected_return_date = datetime.date.today()

        with self.assertRaises(Exception) as raised:
            Borrowing.objects.create(
                expected_return_date=invalid_expected_return_date,
                book=sample_book(),
                user=self.user
            )

        self.assertEqual(IntegrityError, type(raised.exception))

    def test_expected_return_date_gt_borrow_date_accepted(self):
        valid_expected_return_date = datetime.date.today() + datetime.timedelta(days=1)

        borrowing = Borrowing.objects.create(
            expected_return_date=valid_expected_return_date,
            book=sample_book(),
            user=self.user
        )

        self.assertTrue(borrowing)

    def test_expected_return_date_gt_30_days_forbidden(self):
        invalid_expected_return_date = datetime.date.today() + datetime.timedelta(days=31)

        with self.assertRaises(Exception) as raised:
            Borrowing.objects.create(
                expected_return_date=invalid_expected_return_date,
                book=sample_book(),
                user=self.user
            )

        self.assertEqual(IntegrityError, type(raised.exception))

    def test_expected_return_date_lte_30_days_accepted(self):
        valid_expected_return_date = datetime.date.today() + datetime.timedelta(days=30)

        borrowing = Borrowing.objects.create(
            expected_return_date=valid_expected_return_date,
            book=sample_book(),
            user=self.user
        )

        self.assertTrue(borrowing)

    def test_actual_return_date_gt_current_date_forbidden(self):
        expected_return_date = datetime.date.today() + datetime.timedelta(days=4)
        date_gt_current_date = datetime.date.today() + datetime.timedelta(days=1)

        borrowing = Borrowing.objects.create(
                expected_return_date=expected_return_date,
                book=sample_book(),
                user=self.user
            )

        with self.assertRaises(Exception) as raised:
            borrowing.actual_return_date = date_gt_current_date
            borrowing.save()

        self.assertEqual(IntegrityError, type(raised.exception))

    def test_actual_return_date_lt_current_date_forbidden(self):
        expected_return_date = datetime.date.today() + datetime.timedelta(days=4)
        date_lt_current_date = datetime.date.today() - datetime.timedelta(days=1)

        borrowing = Borrowing.objects.create(
                expected_return_date=expected_return_date,
                book=sample_book(),
                user=self.user
            )

        with self.assertRaises(Exception) as raised:
            borrowing.actual_return_date = date_lt_current_date
            borrowing.save()

        self.assertEqual(IntegrityError, type(raised.exception))
