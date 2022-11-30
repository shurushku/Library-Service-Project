import json
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from library.models import Book
from library.serializers import BookListSerializer, BookSerializer


LIBRARY_URL = reverse("library:book-list")


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


def detail_url(book_id):
    return reverse("library:book-detail", args=[book_id])


class PublicLibraryApiTests(TestCase):
    def test_books_list(self):
        sample_book()
        sample_book()

        res = self.client.get(LIBRARY_URL)
        book = Book.objects.all()
        serializer = BookListSerializer(book, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_books_detail(self):
        book = sample_book()

        res = self.client.get(detail_url(book.id))

        serializer = BookSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book(self):
        payload = {
            "title": "Book",
            "author": "Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": 3.99,
        }

        res = self.client.post(LIBRARY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        book = Book.objects.get(id=res.data["id"])

        for key in payload:
            if key == "daily_fee":
                self.assertEqual(payload[key], float(getattr(book, key)))
            else:
                self.assertEqual(payload[key], getattr(book, key))

    # TODO: update and partial_update tests don't work, they raise 415 status code

    # def test_update_book(self):
    #     book = sample_book()
    #     payload = {
    #         "title": "Book",
    #         "author": "Author",
    #         "cover": "SOFT",
    #         "inventory": 3,
    #         "daily_fee": 11.22,
    #     }
    #
    #     res = self.client.put(detail_url(book.id), payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #
    #     book.refresh_from_db()
    #
    #     for key in payload:
    #         if key == "daily_fee":
    #             self.assertEqual(payload[key], float(getattr(book, key)))
    #         else:
    #             self.assertEqual(payload[key], getattr(book, key))
    #
    # def test_partial_update_book(self):
    #     book = sample_book()
    #     payload = {
    #         "inventory": 4,
    #         "daily_fee": 5.99,
    #     }
    #
    #     res = self.client.patch(detail_url(book.id), payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #
    #     book.refresh_from_db()
    #     self.assertEqual(book.inventory, payload["inventory"])
    #     self.assertEqual(float(book.daily_fee), payload["daily_fee"])

    def test_delete_movie_forbidden(self):
        book = sample_book()

        res = self.client.delete(detail_url(book.id))

        books = Book.objects.filter(id=book.id)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(books.count(), 0)
