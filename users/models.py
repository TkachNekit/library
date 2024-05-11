from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_phone_number


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True, validators=[validate_phone_number],
                                    unique=True)
    is_verified_email = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="users_image", null=True, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
