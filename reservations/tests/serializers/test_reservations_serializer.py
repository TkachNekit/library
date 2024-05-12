from datetime import date, timedelta

import pytest

from archive.models import City, Library
from books.models import Author, Book, BookCopy, BookGenre, BookLanguage
from reservations.models import Reservation
from reservations.serializers import ReservationSerializer
from users.models import User


@pytest.mark.django_db
class TestReservationSerializer:
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
        book = TestReservationSerializer.create_book()
        library = TestReservationSerializer.create_library()
        return BookCopy.objects.create(book=book, library=library)

    def create_user(self, username="testuser"):
        return User.objects.create(username=username)

    def test_valid_serializer(self):
        book_copy = self.create_book_copy()
        user = self.create_user()
        data = {
            "book_copy": book_copy.pk,
            "user": user.pk,
            "reservation_date": date.today(),
            "return_date": date.today() + timedelta(days=7),
            "status": Reservation.STATUSES[Reservation.RESERVED][1],
        }
        serializer = ReservationSerializer(data=data)
        assert serializer.is_valid()

    def test_missing_required_fields(self):
        serializer = ReservationSerializer(data={})
        assert not serializer.is_valid()
        assert "book_copy" in serializer.errors
        assert "reservation_date" in serializer.errors
        assert "return_date" in serializer.errors

    def test_create_reservation(self):
        book_copy = self.create_book_copy()
        user = self.create_user()
        data = {
            "book_copy": book_copy.pk,
            "user": user.pk,
            "reservation_date": date.today(),
            "return_date": date.today() + timedelta(days=7),
            "status": Reservation.STATUSES[Reservation.RESERVED][1],
        }
        serializer = ReservationSerializer(data=data)
        assert serializer.is_valid()
        instance = serializer.save()
        assert instance.book_copy == book_copy
        assert instance.user == user
        assert instance.reservation_date == date.today()
        assert instance.return_date == date.today() + timedelta(days=7)
        assert instance.status == Reservation.RESERVED

    def test_invalid_status_choice(self):
        book_copy = self.create_book_copy()
        user = self.create_user()
        data = {
            "book_copy": book_copy.pk,
            "user": user.pk,
            "reservation_date": date.today(),
            "return_date": date.today() + timedelta(days=7),
            "status": 999,
        }
        serializer = ReservationSerializer(data=data)
        assert not serializer.is_valid()
        assert "status" in serializer.errors

    def test_invalid_user(self):
        book_copy = self.create_book_copy()
        data = {
            "book_copy": book_copy.pk,
            "user": 999,  # Invalid user id
            "reservation_date": date.today(),
            "return_date": date.today() + timedelta(days=7),
            "status": Reservation.RESERVED,
        }
        serializer = ReservationSerializer(data=data)
        assert not serializer.is_valid()
        assert "user" in serializer.errors

    def test_invalid_book_copy(self):
        user = self.create_user()
        data = {
            "book_copy": 999,  # Invalid book copy id
            "user": user.pk,
            "reservation_date": date.today(),
            "return_date": date.today() + timedelta(days=7),
            "status": Reservation.RESERVED,
        }
        serializer = ReservationSerializer(data=data)
        assert not serializer.is_valid()
        assert "book_copy" in serializer.errors
