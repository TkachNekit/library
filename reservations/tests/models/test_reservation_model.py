from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError

from archive.models import City, Library
from books.models import Author, Book, BookCopy, BookGenre, BookLanguage
from reservations.models import Reservation
from users.models import User


@pytest.mark.django_db
class TestReservationModel:
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
        book = TestReservationModel.create_book()
        library = TestReservationModel.create_library()
        return BookCopy.objects.create(book=book, library=library)

    def create_reservation(
        self,
        reservation_date=date.today(),
        return_date=date.today() + timedelta(days=7),
    ):
        if BookCopy.objects.all().exists():
            book_copy = BookCopy.objects.get(id=1)
        else:
            book_copy = TestReservationModel.create_book_copy()
        if User.objects.all().exists():
            user = User.objects.get(id=1)
        else:
            user = User.objects.create(username="testuser")
        return Reservation.objects.create(
            book_copy=book_copy,
            user=user,
            reservation_date=reservation_date,
            return_date=return_date,
        )

    def test_create_reservation(self):
        reservation = self.create_reservation()
        assert reservation.pk is not None

    def test_reservation_return_date_earlier_than_reservation_date(self):
        with pytest.raises(ValidationError):
            self.create_reservation(return_date=date.today() - timedelta(days=1))

    def test_reservation_return_date_same_as_reservation_date(self):
        with pytest.raises(ValidationError):
            self.create_reservation(return_date=date.today())

    def test_reservation_overlap_with_existing_reservation(self):
        self.create_reservation(
            reservation_date=date.today(), return_date=date.today() + timedelta(days=7)
        )
        with pytest.raises(ValidationError):
            self.create_reservation(
                reservation_date=date.today() + timedelta(days=3),
                return_date=date.today() + timedelta(days=10),
            )

    def test_reservation_duration_more_than_2_weeks(self):
        with pytest.raises(ValidationError):
            self.create_reservation(return_date=date.today() + timedelta(days=15))

    def test_reservation_duration_exactly_2_weeks(self):
        reservation = self.create_reservation(
            return_date=date.today() + timedelta(days=14)
        )
        assert reservation.pk is not None

    def test_reservation_duration_less_than_2_weeks(self):
        reservation = self.create_reservation(
            return_date=date.today() + timedelta(days=13)
        )
        assert reservation.pk is not None

    def test_reservation_unique(self):
        self.create_reservation()
        with pytest.raises(ValidationError):
            self.create_reservation()
