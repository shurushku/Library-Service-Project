from django.test import TestCase

from library.models import Book


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        book = Book.objects.create(
            title="Book",
            author="Author",
            cover="SOFT",
            inventory=5,
            daily_fee=3.99
        )

        self.assertEqual(
            str(book),
            f"{book.title} ({book.author})"
        )
