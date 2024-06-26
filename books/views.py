from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from books.filters import BookFilter
from books.models import Book, BookCopy, BookGenre, BookLanguage
from books.serializers import (BookCopySerializer, BookGenreSerializer,
                               BookLanguageSerializer, BookSerializer)


class BookViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter


class GenreViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = BookGenre.objects.all()
    serializer_class = BookGenreSerializer


class LanguageViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = BookLanguage.objects.all()
    serializer_class = BookLanguageSerializer


class BookCopyViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = BookCopy.objects.all()
    serializer_class = BookCopySerializer
