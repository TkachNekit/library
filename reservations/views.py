from rest_framework.viewsets import ModelViewSet

from reservations.models import Reservation
from reservations.serializers import ReservationSerializer


class ReservationModelViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
