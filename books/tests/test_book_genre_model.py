import pytest
from django.db.utils import IntegrityError

from books.models import BookGenre


@pytest.mark.django_db
class TestBookGenreModel:
    def test_create_book_genre(self):
        name = "Fantasy"
        genre = BookGenre.objects.create(name=name)
        assert genre.name == name
        assert str(genre) == name

    def test_unique_name_constraint(self):
        name = "Science Fiction"
        BookGenre.objects.create(name=name)
        with pytest.raises(IntegrityError):
            BookGenre.objects.create(
                name=name
            )  # Attempt to create another genre with the same name
