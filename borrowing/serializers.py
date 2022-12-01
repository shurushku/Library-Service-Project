from django.db import transaction
from rest_framework import serializers

from borrowing.models import Borrowing
from library.serializers import BookSerializer
from payment.views import create_payment


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = ("id", "book", "borrow_date", "expected_return_date")

    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs)

        if attrs["book"].inventory == 0:
            raise serializers.ValidationError(
                {"inventory": "no books left in library"}
            )

        return data

    def save(self, **kwargs):
        instance = super(BorrowingSerializer, self).save(**kwargs)

        instance.book.inventory -= 1
        instance.book.save()

        return instance

    def create(self, validated_data):
        with transaction.atomic():
            borrowing = Borrowing.objects.create(**validated_data)
            create_payment(borrowing=borrowing)
            return borrowing


class BorrowingListSerializer(BorrowingSerializer):
    user = serializers.CharField(source="user.email", read_only=True)
    book = serializers.CharField(source="book.title")
    author = serializers.CharField(source="book.author", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
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
