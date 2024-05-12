from datetime import date

import pytest
from django.db import IntegrityError

from archive.models import City
from books.models import Book, BookCopy, BookGenre, BookLanguage, Library


@pytest.fixture
def book_factory():
    def create_book(
        title="Test Book",
        genre_name="Fiction",
        language_name="English",
        publication_date=date(2022, 1, 1),
    ):
        genre = BookGenre.objects.create(name=genre_name)
        language = BookLanguage.objects.create(name=language_name)
        book = Book.objects.create(
            title=title,
            genre=genre,
            language=language,
            publication_date=publication_date,
        )
        city = City.objects.create(name="test city")
        library = Library.objects.create(name="Test Library", city=city)
        book_copy = BookCopy.objects.create(book=book, library=library)
        return book, library, book_copy

    return create_book


@pytest.mark.django_db
class TestBookCopyModel:
    def test_book_copy_str_representation(self, book_factory):
        book, library, book_copy = book_factory()
        assert str(book_copy) == f"{book.title} | {library.name} | {book_copy.id}"

    def test_book_copy_deletion(self, book_factory):
        _, _, book_copy = book_factory()
        book_copy_id = book_copy.id
        book_copy.delete()
        with pytest.raises(BookCopy.DoesNotExist):
            BookCopy.objects.get(pk=book_copy_id)

    def test_book_copy_str_representation_missing_fields(self):
        with pytest.raises(IntegrityError):
            BookCopy.objects.create()

    def test_book_copy_str_representation_missing_book(self, book_factory):
        _, library, _ = book_factory()
        with pytest.raises(IntegrityError):
            BookCopy.objects.create(library=library)

    def test_book_copy_str_representation_missing_library(self, book_factory):
        book, _, _ = book_factory()
        with pytest.raises(IntegrityError):
            BookCopy.objects.create(book=book)

    def test_book_copy_str_representation_missing_both(self):
        with pytest.raises(IntegrityError):
            BookCopy.objects.create()
