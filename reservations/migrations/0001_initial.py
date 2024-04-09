# Generated by Django 4.1.6 on 2024-04-09 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("books", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reservation_date", models.DateField(auto_now_add=True)),
                ("return_date", models.DateField()),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[
                            (0, "Зарезервирована"),
                            (1, "Отменена"),
                            (2, "Возвращена"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "book_copy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="books.bookcopy"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
