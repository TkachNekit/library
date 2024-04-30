from django.urls import path, include
from rest_framework import routers

from books.views import BookViewSet
from reservations.views import ReservationModelViewSet

app_name = 'api'
router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'reservation', ReservationModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
