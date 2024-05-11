import pytest
from django.core.exceptions import ValidationError
from books.models import BookLanguage
from books.serializers import BookLanguageSerializer


@pytest.mark.django_db
class TestBookLanguageSerializer:
    def test_valid_serializer(self):
        data = {'name': 'English'}
        serializer = BookLanguageSerializer(data=data)
        assert serializer.is_valid()

    def test_missing_name(self):
        data = {}
        serializer = BookLanguageSerializer(data=data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors

    def test_blank_name(self):
        data = {'name': ''}
        serializer = BookLanguageSerializer(data=data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors

    def test_unique_name(self):
        BookLanguage.objects.create(name='English')
        data = {'name': 'English'}
        serializer = BookLanguageSerializer(data=data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors

    def test_name_length(self):
        data = {'name': 'A' * 129}  # Exceeds max length
        serializer = BookLanguageSerializer(data=data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors

    def test_create_language(self):
        data = {'name': 'French'}
        serializer = BookLanguageSerializer(data=data)
        assert serializer.is_valid()
        instance = serializer.save()
        assert instance.name == 'French'

    def test_update_language(self):
        language = BookLanguage.objects.create(name='English')
        data = {'name': 'Spanish'}
        serializer = BookLanguageSerializer(language, data=data)
        assert serializer.is_valid()
        instance = serializer.save()
        assert instance.name == 'Spanish'

    def test_invalid_serializer(self):
        data = {'invalid_field': 'value'}  # Invalid field provided
        serializer = BookLanguageSerializer(data=data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors
