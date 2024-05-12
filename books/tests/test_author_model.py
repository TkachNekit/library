import pytest
from django.db.utils import IntegrityError

from books.models import Author


@pytest.mark.django_db
class TestAuthorModel:
    def test_create_author_with_first_and_last_name(self):
        first_name = "John"
        last_name = "Doe"
        author = Author.objects.create(first_name=first_name, last_name=last_name)
        assert author.first_name == first_name
        assert author.last_name == last_name
        assert str(author) == f"{last_name} {first_name}"

    def test_create_author_with_only_first_name(self):
        first_name = "Jane"
        author = Author.objects.create(first_name=first_name)
        assert author.first_name == first_name
        assert author.last_name == ""
        assert str(author) == first_name

    def test_full_name_property(self):
        first_name = "John"
        last_name = "Doe"
        author = Author.objects.create(first_name=first_name, last_name=last_name)
        assert author.full_name == f"{last_name} {first_name}"

    def test_full_name_setter(self):
        author = Author.objects.create(first_name="John")
        author.full_name = "Jane Smith"

        assert author.first_name == "Jane"
        assert author.last_name == "Smith"

    def test_unique_constraint(self):
        first_name = "John"
        last_name = "Doe"
        Author.objects.create(first_name=first_name, last_name=last_name)
        # Attempt to create another author with the same first_name and last_name
        with pytest.raises(IntegrityError):
            Author.objects.create(first_name=first_name, last_name=last_name)
