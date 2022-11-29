from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrIfAuthenticatedReadOnly
from .serializers import PaymentSerializer
from .models import Payment


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    # permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    #
    # def get_queryset(self):
    #     return Payment.objects.filter(borrowing__user=self.request.user)
