from rest_framework import mixins, viewsets, filters
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingDetailSerializer,
    BorrowingListSerializer,
    BorrowingSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["book__title", "id"]

    def get_queryset(self):
        queryset = self.queryset.select_related("book")
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        if is_active:
            if is_active == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            if is_active == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if self.action == "list" and not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
