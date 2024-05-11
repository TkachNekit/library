from datetime import date

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from books.models import Book, BookCopy, BookGenre, BookLanguage, Author
from books.serializers import BookSerializer


@pytest.mark.django_db
class TestBookViewSet:
    @staticmethod
    def create_genre(name: str) -> BookGenre:
        genre = BookGenre.objects.create(name=name)
        return genre

    @staticmethod
    def create_language(name: str) -> BookGenre:
        language = BookLanguage.objects.create(name=name)
        return language

    @staticmethod
    def create_book(title: str,
                    genre: BookGenre = None,
                    language: BookLanguage = None,
                    pub_year: date = date(2022, 1, 1),
                    authors: list[Author.pk] = None) -> Book:
        if genre is None:
            genre = TestBookViewSet.create_genre("test genre")
        if language is None:
            language = TestBookViewSet.create_language("test language")
        if authors is None:
            authors = [Author.objects.create(first_name="John", last_name="Doe")]
        else:
            authors = [Author.objects.get(pk=authors[0])]

        publication_date = pub_year

        book = Book.objects.create(
            title=title,
            genre=genre,
            language=language,
            publication_date=publication_date,
            description="This is a test book",
            number_of_pages=200,
            rating=8.5,
        )
        for a in authors:
            book.authors.add(a)
        return book

    def test_retrieve_book(self):
        book = self.create_book("test title")
        client = APIClient()
        response = client.get(reverse("api:book-detail", kwargs={"pk": book.pk}))
        assert response.status_code == 200
        assert response.data == BookSerializer(instance=book).data

    def test_list_books(self):
        book = self.create_book(title="Book 1")
        book2 = self.create_book(title="Book 2", genre=book.genre, language=book.language, pub_year=date(2021, 1, 1),
                                 authors=[book.authors.get(id=1).pk])
        client = APIClient()
        response = client.get(reverse("api:book-list"))
        assert response.status_code == 200
        assert len(response.data) == 2

    # def test_filter_books_by_genre(self):
    #     book = self.create_book(title="Book 1")
    #     new_genre = TestBookViewSet.create_genre("new genre")
    #     book2 = self.create_book(title="Book 2", genre=new_genre, language=book.language, pub_year=date(2021, 1, 1),
    #                              authors=[book.authors.get(id=1).pk])
    #     client = APIClient()
    #     response = client.get(reverse("api:book-list"), {"genre": new_genre.name})
    #     assert response.status_code == 200
    #     assert len(response.data) == 1
    #
    # def test_filter_books_by_language(self):
    #     self.create_book(title="Book 1", language="English")
    #     self.create_book(title="Book 2", language="French")
    #     client = APIClient()
    #     response = client.get(reverse("api:book-list"), {"language": "English"})
    #     assert response.status_code == 200
    #     assert len(response.data) == 1
