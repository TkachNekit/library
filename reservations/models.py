from datetime import date

from django.core.exceptions import ValidationError
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
    reservation_date = models.DateField(auto_now_add=True, null=False, blank=False)
    return_date = models.DateField(null=False, blank=False)
    status = models.SmallIntegerField(default=RESERVED, choices=STATUSES)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"{self.book_copy.book.title} | {self.book_copy.library.name} | {self.reservation_date} | " \
               f"{self.return_date}"

    def save(self, *args, **kwargs):
        if date.today() >= self.return_date:
            raise ValidationError("Return date cannot be today or earlier")
        super().save(*args, **kwargs)

    def clean(self):
        # check if this book copy is not already reserved on this dates
        pass
        # existing_reservations = Reservation.objects.filter(
        #     book_copy=self.book_copy,
        #     reservation_date=self.reservation_date,
        #     return_date=self.return_date,
        #     status=self.RESERVED
        # )
        # if self.pk:  # Если это обновление объекта, нужно исключить текущий объект из поиска
        #     existing_reservations = existing_reservations.exclude(pk=self.pk)
        # if existing_reservations.exists():
        #     raise ValidationError("Reservation with the same book copy and dates already exists.")
