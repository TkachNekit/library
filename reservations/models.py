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

    def save(self, *args, **kwargs):
        if self.reservation_date >= self.return_date:
            raise ValidationError("Reservation date cannot be greater or equal to return date")
        super().save(*args, **kwargs)
