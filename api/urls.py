from django.urls import include, path
from rest_framework import routers

from archive.views import LibraryViewSet
from books.views import (BookCopyViewSet, BookViewSet, GenreViewSet,
                         LanguageViewSet)
from reservations.views import ReservationModelViewSet

app_name = "api"
router = routers.DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"reservations", ReservationModelViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"languages", LanguageViewSet)
router.register(r"bookcopies", BookCopyViewSet)
router.register(r"libraries", LibraryViewSet, basename="library")

urlpatterns = [
    path("", include(router.urls)),
]
