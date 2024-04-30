from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from books.filters import BookFilter
from books.models import Book
from books.serializers import BookSerializer


class BookViewSet(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

