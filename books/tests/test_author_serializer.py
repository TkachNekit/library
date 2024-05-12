import pytest

from books.models import Author
from books.serializers import AuthorSerializer


@pytest.mark.django_db
class TestAuthorSerializer:
    def test_valid_serializer(self):
        data = {"first_name": "John", "last_name": "Doe"}
        serializer = AuthorSerializer(data=data)
        assert serializer.is_valid()

    def test_missing_first_name(self):
        data = {"last_name": "Doe"}
        serializer = AuthorSerializer(data=data)
        assert not serializer.is_valid()
        assert "first_name" in serializer.errors

    def test_blank_first_name(self):
        data = {"first_name": "", "last_name": "Doe"}
        serializer = AuthorSerializer(data=data)
        assert not serializer.is_valid()
        assert "first_name" in serializer.errors

    def test_missing_last_name(self):
        data = {"first_name": "John", "last_name": ""}
        serializer = AuthorSerializer(data=data)
        assert serializer.is_valid()

    def test_create_author(self):
        data = {"first_name": "Jane", "last_name": "Doe"}
        serializer = AuthorSerializer(data=data)
        assert serializer.is_valid()
        instance = serializer.save()
        assert instance.first_name == "Jane"
        assert instance.last_name == "Doe"

    def test_unique_together_constraint(self):
        Author.objects.create(first_name="John", last_name="Doe")
        data = {"first_name": "John", "last_name": "Doe"}
        serializer = AuthorSerializer(data=data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_invalid_serializer(self):
        data = {"invalid_field": "value"}  # Invalid field provided
        serializer = AuthorSerializer(data=data)
        assert not serializer.is_valid()
        assert "first_name" in serializer.errors
