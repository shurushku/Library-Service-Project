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
        Book,
        on_delete=models.CASCADE,
        related_name="books"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="users"
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
