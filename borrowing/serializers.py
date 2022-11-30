from rest_framework import serializers

from borrowing.models import Borrowing
from library.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = ("book", "borrow_date", "expected_return_date", "user")


class BorrowingListSerializer(BorrowingSerializer):
    user = serializers.CharField(source="user.email", read_only=True)
    book = serializers.CharField(source="book.title")
    author = serializers.CharField(source="book.author", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "book",
            "author",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )
        read_only_fields = ("actual_return_date",)


class BorrowingDetailSerializer(BorrowingListSerializer):
    book = BookSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )
