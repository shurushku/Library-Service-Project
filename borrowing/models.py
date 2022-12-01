import datetime

from django.conf import settings
from django.db import models
from django.db.models import F, Q, CheckConstraint

from library.models import Book
from user.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=(
                    Q(expected_return_date__gt=F("borrow_date"))
                    & Q(expected_return_date__lte=(
                        datetime.date.today()
                        + datetime.timedelta(days=30)))
                ),
                name="check_expected_return_date",
            ),
            CheckConstraint(
                check=Q(actual_return_date=datetime.date.today()),
                name="check_actual_return_date",
            ),
        ]

    def get_total_price(self, payment_type: str) -> str:
        book_price = self.book.daily_fee
        if payment_type == "PAYMENT":
            count_of_days = self.expected_return_date - self.borrow_date
        if payment_type == "FINE":
            count_of_days = self.actual_return_date - self.expected_return_date
        return str(round(book_price * count_of_days.days, 2))
