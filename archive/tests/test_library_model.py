import pytest
from django.db import IntegrityError
from archive.models import Library, City


@pytest.mark.django_db
class TestLibraryModel:

    def test_create_library(self):
        city = City.objects.create(name='Test City')
        library = Library.objects.create(name='Test Library', city=city)
        assert library.name == 'Test Library'
        assert library.city == city

    def test_unique_name_constraint(self):
        city = City.objects.create(name='Test City')
        Library.objects.create(name='Test Library', city=city)
        with pytest.raises(IntegrityError):
            Library.objects.create(name='Test Library', city=city)

    def test_str_representation(self):
        city = City.objects.create(name='Test City')
        library = Library.objects.create(name='Test Library', city=city)
        assert str(library) == 'Test Library | Test City'
