from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from archive.models import Library
from archive.serializers import LibrarySerializer


class LibraryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
