from django.contrib import admin

from reservations.models import Reservation


# admin.site.register(Reservation)
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("book_copy", "user", "reservation_date", "return_date", "status",)
    fields = ("id", "book_copy", "user", ("reservation_date", "return_date"), "status")
    readonly_fields = ("id",)


class ReservationInlineAdmin(admin.TabularInline):
    model = Reservation
    fields = ("book_copy", "user", ("reservation_date", "return_date"), "status")
    extra = 0