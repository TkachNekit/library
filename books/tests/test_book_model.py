from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from books.models import Author, Book, BookGenre, BookLanguage


@pytest.mark.django_db
class TestBookModel:
    def test_create_book(self):
        genre = BookGenre.objects.create(name="Fiction")
        language = BookLanguage.objects.create(name="English")
        author = Author.objects.create(first_name="John", last_name="Doe")
        title = "Test Book"
        publication_date = date(2022, 1, 1)
        description = "This is a test book"
        number_of_pages = 200
        rating = 8.5

        book = Book.objects.create(
            title=title,
            genre=genre,
            language=language,
            publication_date=publication_date,
            description=description,
            number_of_pages=number_of_pages,
            rating=rating,
        )
        book.authors.add(author)

        assert book.title == title
        assert book.genre == genre
        assert book.language == language
        assert book.publication_date == publication_date
        assert book.description == description
        assert book.number_of_pages == number_of_pages
        assert book.rating == rating

    def test_str_representation(self):
        title = "Test Book"
        genre = BookGenre.objects.create(name="Fiction")
        language = BookLanguage.objects.create(name="English")
        publication_date = date(2022, 1, 1)
        book = Book.objects.create(
            title=title,
            genre=genre,
            language=language,
            publication_date=publication_date,
        )
        assert str(book) == f"{title} | {publication_date.year} | {language}"

    def test_invalid_rating(self):
        genre = BookGenre.objects.create(name="Fiction")
        language = BookLanguage.objects.create(name="English")
        publication_date = date(2022, 1, 1)

        # Attempt to create a book with an invalid rating
        with pytest.raises(ValidationError):
            Book.objects.create(
                title="Test Book",
                genre=genre,
                language=language,
                publication_date=publication_date,
                rating=15,  # Invalid rating
            )

    def test_add_and_remove_authors(self):
        genre = BookGenre.objects.create(name="Fiction")
        language = BookLanguage.objects.create(name="English")
        author1 = Author.objects.create(first_name="Jane", last_name="Doe")
        author2 = Author.objects.create(first_name="Jack", last_name="Smith")
        publication_date = date(2022, 1, 1)
        book = Book.objects.create(
            title="Test Book",
            genre=genre,
            language=language,
            publication_date=publication_date,
        )
        book.authors.add(author1)
        book.authors.add(author2)
        assert author1 in book.authors.all()
        assert author2 in book.authors.all()
        book.authors.remove(author1)
        assert author1 not in book.authors.all()

    def test_missing_required_fields(self):
        genre = BookGenre.objects.create(name="Fiction")
        language = BookLanguage.objects.create(name="English")
        publication_date = date(2022, 1, 1)

        # Attempt to create a book with missing required fields
        with pytest.raises(ValidationError):
            Book.objects.create(
                genre=genre,
                language=language,
                publication_date=publication_date,
            )

    def test_update_existing_book(self):
        genre = BookGenre.objects.create(name="Fiction")
        language = BookLanguage.objects.create(name="English")
        author = Author.objects.create(first_name="John", last_name="Doe")
        publication_date = date(2022, 1, 1)
        book = Book.objects.create(
            title="Test Book",
            genre=genre,
            language=language,
            publication_date=publication_date,
        )
        book.authors.add(author)

        new_title = "Updated Title"
        new_description = "Updated description"
        book.title = new_title
        book.description = new_description
        book.save()

        updated_book = Book.objects.get(pk=book.pk)
        assert updated_book.title == new_title
        assert updated_book.description == new_description

    def test_query_books_by_criteria(self):
        genre = BookGenre.objects.create(name="Fiction")
        language1 = BookLanguage.objects.create(name="English")
        language2 = BookLanguage.objects.create(name="French")
        publication_date = date(2022, 1, 1)
        Book.objects.create(
            title="Book 1",
            genre=genre,
            language=language1,
            publication_date=publication_date,
        )
        Book.objects.create(
            title="Book 2",
            genre=genre,
            language=language2,
            publication_date=publication_date,
        )
        Book.objects.create(
            title="Book 3",
            genre=genre,
            language=language1,
            publication_date=publication_date,
        )
        books_in_english = Book.objects.filter(language=language1)
        assert books_in_english.count() == 2

    def test_sort_books(self):
        genre = BookGenre.objects.create(name="Fiction")
        language = BookLanguage.objects.create(name="English")
        publication_date1 = date(2022, 1, 1)
        publication_date2 = date(2021, 1, 1)
        Book.objects.create(
            title="Book 1",
            genre=genre,
            language=language,
            publication_date=publication_date1,
        )
        Book.objects.create(
            title="Book 2",
            genre=genre,
            language=language,
            publication_date=publication_date2,
        )
        books_sorted_by_date = Book.objects.order_by("publication_date")
        assert books_sorted_by_date[0].title == "Book 2"

    def test_future_publication_date(self):
        genre = BookGenre.objects.create(name="Fiction")
        language = BookLanguage.objects.create(name="English")
        future_publication_date = date.today() + timedelta(days=30)

        # Attempt to create a book with a future publication date
        with pytest.raises(ValidationError):
            Book.objects.create(
                title="Test Book",
                genre=genre,
                language=language,
                publication_date=future_publication_date,
            )

    def test_negative_number_of_pages(self):
        genre = BookGenre.objects.create(name="Fiction")
        language = BookLanguage.objects.create(name="English")
        publication_date = date(2022, 1, 1)

        # Attempt to create a book with a negative number of pages
        with pytest.raises(IntegrityError):
            Book.objects.create(
                title="Test Book",
                genre=genre,
                language=language,
                publication_date=publication_date,
                number_of_pages=-100,  # Negative number of pages
            )

    def test_non_unique_title(self):
        genre = BookGenre.objects.create(name="Fiction")
        language = BookLanguage.objects.create(name="English")
        publication_date = date(2022, 1, 1)
        Book.objects.create(
            title="Test Book",
            genre=genre,
            language=language,
            publication_date=publication_date,
        )

        # Attempt to create a book with a non-unique title
        with pytest.raises(ValidationError):
            Book.objects.create(
                title="Test Book",  # Duplicate title
                genre=genre,
                language=language,
                publication_date=publication_date,
            )

    # def test_missing_cover_image(self):
    #     genre = BookGenre.objects.create(name="Fiction")
    #     language = BookLanguage.objects.create(name="English")
    #     publication_date = date(2022, 1, 1)
    #
    #     # Attempt to create a book with a missing cover image
    #     book = Book.objects.create(
    #         title="Test Book",
    #         genre=genre,
    #         language=language,
    #         publication_date=publication_date,
    #     )
    #     assert book.cover is None
