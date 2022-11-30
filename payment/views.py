from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from rest_framework.permissions import IsAuthenticated
from .serializers import PaymentSerializer
from .models import Payment


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing__user=self.request.user)
