from django.urls import path, include
from rest_framework import routers

from archive.views import LibraryViewSet
from books.views import BookViewSet, GenreViewSet, LanguageViewSet, BookCopyViewSet
from reservations.views import ReservationModelViewSet

app_name = 'api'
router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'reservations', ReservationModelViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'bookcopies', BookCopyViewSet)
router.register(r'libraries', LibraryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
