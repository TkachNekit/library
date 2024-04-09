from django.db import models


class City(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Library(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Библиотека"
        verbose_name_plural = "Библиотеки"
