from django.test import TestCase

from archive.models import City, Library
from archive.serializers import LibrarySerializer


class LibrarySerializerTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Test City")

    def test_valid_data(self):
        serializer = LibrarySerializer(
            data={"name": "Test Library", "city": self.city.name}
        )
        self.assertTrue(serializer.is_valid())

    def test_missing_name(self):
        serializer = LibrarySerializer(data={"city": self.city.name})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["name"], ["This field is required."])

    def test_missing_city(self):
        serializer = LibrarySerializer(data={"name": "Test Library"})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["city"], ["This field is required."])

    def test_invalid_city(self):
        serializer = LibrarySerializer(
            data={"name": "Test Library", "city": "Nonexistent City"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["city"],
            ["Object with name=Nonexistent City does not exist."],
        )

    def test_duplicate_name(self):
        Library.objects.create(name="Test Library", city=self.city)
        serializer = LibrarySerializer(
            data={"name": "Test Library", "city": self.city.name}
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["name"], ["Библиотека with this name already exists."]
        )
