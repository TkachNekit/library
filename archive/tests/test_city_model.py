from django.db import IntegrityError
from django.test import TestCase

from archive.models import City


class CityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        City.objects.create(name="Test City")

    def test_name_label(self):
        city = City.objects.get(id=1)
        field_label = city._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        city = City.objects.get(id=1)
        max_length = city._meta.get_field("name").max_length
        self.assertEqual(max_length, 128)

    def test_str_representation(self):
        city = City.objects.get(id=1)
        self.assertEqual(str(city), "Test City")

    def test_name_unique(self):
        # Attempt to create a City with the same name as an existing one
        with self.assertRaises(IntegrityError):
            City.objects.create(name="Test City")
