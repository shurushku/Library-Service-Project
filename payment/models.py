from django.db import models


class Payment(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
    )
    TYPE_CHOICES = (
        ("PAYMENT", "Payment"),
        ("FINE", "Fine"),
    )

    status = models.CharField(
        max_length=7, choices=STATUS_CHOICES, default="PENDING"
    )
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    borrowing = models.CharField(max_length=255)
    # borrowing = models.OneToOneField(to=Borrowing)
    session_url = models.URLField()
    session_id = models.TextField()
    money_to_pay = models.IntegerField()

