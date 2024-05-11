from datetime import date

import pytest
from django.db.utils import IntegrityError

from archive.models import City
from books.models import Book, BookCopy, Library, BookGenre, BookLanguage, Author
from books.serializers import BookCopySerializer


@pytest.mark.django_db
class TestBookCopySerializer:
    @staticmethod
    def create_book():
        genre = BookGenre.objects.create(name="Fiction")
        language = BookLanguage.objects.create(name="English")
        author = Author.objects.create(first_name="John", last_name="Doe")
        publication_date = date(2022, 1, 1)

        book = Book.objects.create(
            title="Test Book",
            genre=genre,
            language=language,
            publication_date=publication_date,
            description="This is a test book",
            number_of_pages=200,
            rating=8.5,
        )
        book.authors.add(author)
        return book

    @staticmethod
    def create_library():
        city = City.objects.create(name="test_city")
        library = Library.objects.create(name="Test Library", city=city)
        return library

    @staticmethod
    def create_book_copy():
        book = TestBookCopySerializer.create_book()
        library = TestBookCopySerializer.create_library()
        return BookCopy.objects.create(book=book, library=library)

    def test_valid_serializer(self):
        book_copy = self.create_book_copy()
        data = BookCopySerializer(instance=book_copy).data
        data['book'] = None  # Modify book to test serializer
        serializer = BookCopySerializer(data=data)
        assert not serializer.is_valid()

    def test_missing_required_fields(self):
        serializer = BookCopySerializer(data={})
        assert not serializer.is_valid()
        assert 'book' in serializer.errors
        assert 'library' in serializer.errors

    def test_create_book_copy(self):
        book = TestBookCopySerializer.create_book()
        library = TestBookCopySerializer.create_library()
        serializer = BookCopySerializer(data={'book': book.id, 'library': library.id})
        assert serializer.is_valid()
        instance = serializer.save()
        assert instance.book.title == "Test Book"
        assert instance.library.name == "Test Library"

    def test_invalid_book_copy(self):
        book = TestBookCopySerializer.create_book()
        serializer = BookCopySerializer(data={'book': book.id, 'library': None})
        assert not serializer.is_valid()
        assert 'library' in serializer.errors

    def test_unique_book_copy(self):
        book = TestBookCopySerializer.create_book()
        library = TestBookCopySerializer.create_library()
        BookCopy.objects.create(book=book, library=library)
        BookCopy.objects.create(book=book, library=library)
        assert len(BookCopy.objects.filter(book=book, library=library)) == 2

    def test_book_copy_deletion(self):
        book_copy = self.create_book_copy()
        book_copy_id = book_copy.id
        book_copy.delete()
        with pytest.raises(BookCopy.DoesNotExist):
            BookCopy.objects.get(pk=book_copy_id)

    def test_book_copy_str_representation(self):
        book_copy = self.create_book_copy()
        assert str(book_copy) == f"{book_copy.book.title} | {book_copy.library.name} | {book_copy.id}"

