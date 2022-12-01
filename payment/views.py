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
stripe.api_key = os.environ.get("STRIPE_API_KEY", "")


def create_session(book_title: str, unit_amount: int) -> (str, str):
    if stripe.api_key:
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
            success_url=SUCCESS_URL,
            cancel_url=CANCEL_URL,
        )
        return session.url, session.id
    return "", ""


def create_payment(borrowing: Borrowing, payment_type: str):
    money_to_pay = borrowing.get_total_price(payment_type)
    book_title = borrowing.book.title
    unit_amount = int(money_to_pay.replace(".", ""))
    session_url, session_id = create_session(book_title, unit_amount)

    Payment.objects.create(
        borrowing=borrowing,
        payment_status="PENDING",
        payment_type=payment_type,
        session_url=session_url,
        session_id=session_id,
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
