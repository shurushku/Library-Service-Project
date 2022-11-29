import datetime

from django.db import models
from user.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    # book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name="books")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")

    def clean(self):
        self.expected_return_date = self.borrow_date + datetime.timedelta(days=10)

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )
