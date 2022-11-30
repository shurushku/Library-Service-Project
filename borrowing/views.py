from rest_framework import mixins, generics

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingDetailSerializer,
    BorrowingListSerializer,
    BorrowingSerializer,
)


class BorrowingList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = BorrowingSerializer
        return self.create(request, *args, **kwargs)


class BorrowingDetail(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
