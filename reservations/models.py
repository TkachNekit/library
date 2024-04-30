import datetime
from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

from books.models import BookCopy
from users.models import User


class Reservation(models.Model):
    RESERVED = 0
    CANCELED = 1
    RETURNED = 2

    STATUSES = (
        (RESERVED, 'Зарезервирована'),
        (CANCELED, 'Отменена'),
        (RETURNED, 'Возвращена'),
    )

    book_copy = models.ForeignKey(to=BookCopy, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    reservation_date = models.DateField(null=False, blank=False)
    return_date = models.DateField(null=False, blank=False)
    status = models.SmallIntegerField(default=RESERVED, choices=STATUSES)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"{self.book_copy.book.title} | {self.book_copy.library.name} | {self.reservation_date} | " \
               f"{self.return_date}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        super().full_clean()
        # Reservation > 1 day
        if self.reservation_date >= self.return_date:
            raise ValidationError(_("Return date cannot be earlier than 1 after reservation"))

        # Book is already booked on these dates
        current_book_reservations = Reservation.objects.filter(status=self.RESERVED, book_copy=self.book_copy)
        for reservation in current_book_reservations:
            take_date, return_date = reservation.reservation_date, reservation.return_date
            if (take_date < self.return_date <= return_date) or (take_date <= self.reservation_date < return_date) or \
                    (self.return_date > return_date and self.reservation_date < take_date):
                raise ValidationError(_("There is already reservation for this book on these dates"))

        # Can't take book for more than 2 weeks
        if (self.return_date - self.reservation_date) > datetime.timedelta(days=14):
            raise ValidationError(_("You can't reserve for more than 2 weeks"))

    def validate_unique(self, exclude=None):
        super(Reservation, self).validate_unique()
