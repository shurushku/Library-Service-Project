import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingListSerializer, BorrowingDetailSerializer
from library.models import Book

BORROWING_URL = reverse("borrowing:borrowing-list")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def sample_expected_return_date(days: int):
    return datetime.date.today() + datetime.timedelta(days=days)


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
        "expected_return_date": sample_expected_return_date(3),
        "book": sample_book(),
        "user": params["user"]
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)


def detail_url(borrowing_id):
    return reverse("borrowing:borrowing-detail", args=[borrowing_id])


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required_movies_list(self):
        res = self.client.get(BORROWING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_borrowings_list_only_users_borrowings(self):
        other_client = create_user(
            email="test1@test.com",
            password="test1pass",
        )
        sample_borrowing(user=self.user)
        sample_borrowing(user=other_client)

        res = self.client.get(BORROWING_URL)
        borrowing = Borrowing.objects.filter(user_id=self.user.id)
        serializer = BorrowingListSerializer(borrowing, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_borrowings_detail(self):
        borrowing = sample_borrowing(user=self.user)

        res = self.client.get(detail_url(borrowing.id))

        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_borrowing_with_current_user(self):
        book = sample_book()
        payload = {
            "expected_return_date": sample_expected_return_date(7),
            "book": book.id,
        }

        res = self.client.post(BORROWING_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        borrowing = Borrowing.objects.get(id=res.data["id"])

        self.assertEqual(payload["expected_return_date"], borrowing.expected_return_date)
        self.assertEqual(payload["book"], borrowing.book_id)
        self.assertEqual(self.user, borrowing.user)

    def test_create_borrowing_with_0_inventory_forbidden(self):
        book = sample_book(inventory=0)
        payload = {
            "expected_return_date": sample_expected_return_date(7),
            "book": book.id,
        }

        res = self.client.post(BORROWING_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_borrowing_decreasing_book_inventory_by_1(self):
        start_inventory = 3
        book = sample_book(inventory=start_inventory)
        payload = {
            "expected_return_date": sample_expected_return_date(7),
            "book": book.id,
        }

        self.client.post(BORROWING_URL, payload)

        book.refresh_from_db()

        self.assertEqual(book.inventory, start_inventory - 1)


class AdminMovieApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            "admin.user@cinema.com",
            "admin.user1234",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_borrowings_list_all_borrowings(self):
        other_client = create_user(
            email="test1@test.com",
            password="test1pass",
        )
        sample_borrowing(user=self.user)
        sample_borrowing(user=other_client)

        res = self.client.get(BORROWING_URL)
        borrowing = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowing, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_borrowing_forbidden(self):
        borrowing = sample_borrowing(user=self.user)

        book = sample_book(title="Test book")
        payload = {
            "expected_return_date": sample_expected_return_date(7),
            "book": book.id,
        }

        res = self.client.put(detail_url(borrowing.id), payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update_borrowing_forbidden(self):
        borrowing = sample_borrowing(user=self.user)

        payload = {
            "expected_return_date": sample_expected_return_date(7),
        }

        res = self.client.put(detail_url(borrowing.id), payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_movie_forbidden(self):
        borrowing = sample_borrowing(user=self.user)

        res = self.client.delete(detail_url(borrowing.id))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
