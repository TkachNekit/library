from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from reservations.models import Reservation
from reservations.serializers import ReservationSerializer


class ReservationModelViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            user_id = self.request.user.id
            request.data["user"] = user_id
            serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except ValidationError as e:
            return Response(e, status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        data = super(ReservationModelViewSet, self).list(request, *args, **kwargs)
        return data
