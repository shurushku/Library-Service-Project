from django.urls import path, include

from borrowing.views import BorrowingList, BorrowingDetail


urlpatterns = [
    path("borrowings/", BorrowingList.as_view(), name="borrowing-list"),
    path(
        "borrowings/<int:pk>/",
        BorrowingDetail.as_view(),
        name="borrowing-detail"
    ),
]

app_name = "borrowing"
