import pytest
from datetime import date
from books.models import Book, BookGenre, BookLanguage, Author
from books.serializers import BookSerializer


@pytest.mark.django_db
class TestBookSerializer:
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

    def test_valid_serializer(self):
        book = self.create_book()
        data = BookSerializer(instance=book).data
        data['title'] = "New Title"
        serializer = BookSerializer(data=data)
        assert serializer.is_valid()

    def test_missing_required_fields(self):
        serializer = BookSerializer(data={})
        assert not serializer.is_valid()
        assert 'title' in serializer.errors
        assert 'genre' in serializer.errors
        assert 'language' in serializer.errors
        assert 'publication_date' in serializer.errors

    def test_invalid_publication_date(self):
        serializer = BookSerializer(data={'title': 'Test Book',
                                          'genre': 'Fiction',
                                          'language': 'English',
                                          'publication_date': '2050-01-01'})
        assert not serializer.is_valid()
        assert 'publication_date' in serializer.errors

    def test_create_book(self):
        language = BookLanguage.objects.create(name='English')
        genre = BookGenre.objects.create(name='Fiction')
        author1 = Author.objects.create(first_name='first_name1', last_name='last_name1')
        author2 = Author.objects.create(first_name='first_name2', last_name='last_name2')
        serializer = BookSerializer(data={'title': 'Test Book',
                                          'genre': genre.id,
                                          'language': language.id,
                                          'publication_date': '2022-01-01',
                                          'authors': [author1.id, author2.id]})
        assert serializer.is_valid()
        instance = serializer.save()
        assert instance.title == 'Test Book'
        assert instance.genre.name == 'Fiction'
        assert instance.language.name == 'English'
        assert instance.publication_date == date(2022, 1, 1)
