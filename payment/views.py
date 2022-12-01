import os
import stripe

from dotenv import load_dotenv
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from rest_framework.permissions import IsAuthenticated
from .serializers import PaymentSerializer
from .models import Payment
from borrowing.models import Borrowing


SUCCESS_URL = "http://127.0.0.1:8000/api/payment/success"
CANCEL_URL = "http://127.0.0.1:8000/api/payment/cancel"
load_dotenv()
stripe.api_key = os.environ.get("STRIPE_API_KEY")


def _get_money_to_pay(borrowing: Borrowing) -> str:
    book_price = borrowing.book.daily_fee
    start_date = borrowing.borrow_date
    end_date = borrowing.expected_return_date
    count_of_days = end_date - start_date
    return str(round(book_price * count_of_days.days, 2))


def create_payment(borrowing: Borrowing):
    money_to_pay = _get_money_to_pay(borrowing)
    book_title = borrowing.book.title
    unit_amount = int(money_to_pay.replace(".", ""))
    session = stripe.checkout.Session.create(
        # customer_email=self.request.user.email,
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": book_title},
                "unit_amount": unit_amount,
            },
            "quantity": 1
        }],
        mode="payment",
        success_url=SUCCESS_URL,
        cancel_url=CANCEL_URL,
    )

    Payment.objects.create(
        borrowing=borrowing,
        payment_status="PENDING",
        payment_type="PAYMENT",
        session_url=session.url,
        session_id=session.id,
        money_to_pay=float(money_to_pay),
    )


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = Payment.objects.filter(
                borrowing__user=self.request.user
            )

        return queryset
