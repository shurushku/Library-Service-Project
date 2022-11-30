from django.db import transaction
from rest_framework import serializers

from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("borrow_date", "expected_return_date", "actual_return_date")