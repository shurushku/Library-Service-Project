from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "payment_status",
            "payment_type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentBorrowingSerializer(PaymentSerializer):
    class Meta:
        model = Payment
        fields = (
            "payment_status",
            "payment_type",
            "session_url",
            "session_id",
            "money_to_pay",
        )
