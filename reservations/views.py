from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from books.models import BookCopy
from books.serializers import BookCopySerializer
from reservations.models import Reservation
from reservations.serializers import ReservationSerializer


class ReservationModelViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # request.data['user'] = self.request.user.username
        # request.data['status'] = "Зарезервирована"
        # if not BookCopy.objects.filter(id=request.data['book_copy']).exists():
        #     return Response("In book_copy should be represented book copy id.", status.HTTP_404_NOT_FOUND)
        # request.data['book_copy'] = BookCopySerializer(instance=BookCopy.objects.get(id=request.data['book_copy'])).data
        # print(request.data)
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
