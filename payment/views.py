import os
import stripe

from dotenv import load_dotenv
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from rest_framework.permissions import IsAuthenticated
from .serializers import (
    PaymentSerializer,
    PaymentDetailSerializer,
    PaymentCreateSerializer,
)
from .models import Payment
from borrowing.models import Borrowing


load_dotenv()
stripe.api_key = os.environ.get("STRIPE_API_KEY", "")


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    SUCCESS_URL = "http://127.0.0.1:8000/api/payment/success"
    CANCEL_URL = "http://127.0.0.1:8000/api/payment/cancel"
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PaymentDetailSerializer
        if self.action == "create":
            return PaymentCreateSerializer
        return PaymentSerializer

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = Payment.objects.filter(
                borrowing__user=self.request.user
            )

        return queryset

    # This function is just for start. Will be changed in the future.
    @staticmethod
    def _get_money_to_pay(borrowing: Borrowing) -> str:
        book_price = borrowing.book.daily_fee
        start_date = borrowing.borrow_date
        end_date = borrowing.expected_return_date
        count_of_days = end_date - start_date
        return str(round(book_price * count_of_days.days, 2))

    # This perform_create only for this task.
    # That why I think tests don't needed
    def perform_create(self, serializer):
        borrowing = Borrowing.objects.get(id=self.request.POST["borrowing"])
        money_to_pay = self._get_money_to_pay(borrowing)
        book_title = borrowing.book.title
        unit_amount = int(money_to_pay.replace(".", ""))
        session = stripe.checkout.Session.create(
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": book_title},
                    "unit_amount": unit_amount,
                },
                "quantity": 1
            }],
            mode="payment",
            success_url=self.SUCCESS_URL,
            cancel_url=self.CANCEL_URL,
        )

        serializer.save(
            session_url=session.url,
            session_id=session.id,
            money_to_pay=float(money_to_pay),
        )
