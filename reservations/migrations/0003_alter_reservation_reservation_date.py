# Generated by Django 4.2.11 on 2024-04-29 16:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reservations", "0002_alter_reservation_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="reservation_date",
            field=models.DateField(),
        ),
    ]
