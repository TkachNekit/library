import pytest
from django.db.utils import IntegrityError
from books.models import BookLanguage


@pytest.mark.django_db
class TestBookLanguageModel:
    def test_create_book_language(self):
        name = "English"
        language = BookLanguage.objects.create(name=name)
        assert language.name == name
        assert str(language) == name

    def test_unique_name_constraint(self):
        name = "Spanish"
        BookLanguage.objects.create(name=name)
        with pytest.raises(IntegrityError):
            BookLanguage.objects.create(name=name)  # Attempt to create another language with the same name
