from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status",
            "pay_type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay"
        )
