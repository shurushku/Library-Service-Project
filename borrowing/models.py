import datetime

from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_created=True)
    expected_return_date = borrow_date
                           # + datetime.timedelta(days=30)
    actual_return_date = models.DateField(auto_now_add=True)
    # book_id = models.OneToOneField(Book, on_delete=models.CASCADE, related_name="books")
    # user_id = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, related_name="users")
