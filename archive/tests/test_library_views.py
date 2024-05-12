from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from archive.models import City, Library
from archive.serializers import LibrarySerializer


class LibraryViewSetTest(APITestCase):
    def setUp(self):
        self.city = City.objects.create(name="Test City")
        self.library1 = Library.objects.create(name="Library 1", city=self.city)
        self.library2 = Library.objects.create(name="Library 2", city=self.city)

    def test_list_libraries(self):
        url = reverse("api:library-list")
        response = self.client.get(url)
        libraries = Library.objects.all()
        serializer = LibrarySerializer(libraries, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_library(self):
        url = reverse("api:library-detail", kwargs={"pk": self.library1.pk})
        response = self.client.get(url)
        library = Library.objects.get(pk=self.library1.pk)
        serializer = LibrarySerializer(library)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # Add more test cases as needed
