from rest_framework import serializers

from books.models import BookCopy
from reservations.models import Reservation
from users.models import User


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, value):
        if value == "" and self.allow_blank:
            return value
        return self._choices[value]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == "" and self.allow_blank:
            return ""

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail("invalid_choice", input=data)


class ReservationSerializer(serializers.ModelSerializer):
    book_copy = serializers.PrimaryKeyRelatedField(
        required=True, queryset=BookCopy.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        required=False, queryset=User.objects.all()
    )
    status = ChoiceField(choices=Reservation.STATUSES, required=False)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "book_copy",
            "user",
            "reservation_date",
            "return_date",
            "status",
        ]
        read_only_fields = ["id"]
