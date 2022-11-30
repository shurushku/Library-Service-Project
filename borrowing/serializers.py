from rest_framework import serializers

from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Borrowing
        fields = ("book", "borrow_date", "expected_return_date", "user")


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.CharField(source="book.title", read_only=True)
    author = serializers.CharField(source="book.author", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "book",
            "author",
            "user",
            "borrow_date",
            "expected_return_date"
        )


class BorrowingDetailSerializer(BorrowingListSerializer):
    cover = serializers.CharField(source="book.cover", read_only=True)
    inventory = serializers.IntegerField(
        source="book.inventory",
        read_only=True
    )
    daily_fee = serializers.DecimalField(
        source="book.daily_fee",
        read_only=True,
        max_digits=6,
        decimal_places=2
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "author",
            "cover",
            "inventory",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "daily_fee",
        )
