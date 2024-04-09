from django.contrib import admin

from reservations.admin import ReservationInlineAdmin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (ReservationInlineAdmin,)
