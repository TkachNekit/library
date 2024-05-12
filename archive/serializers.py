from rest_framework import serializers

from archive.models import City, Library


class LibrarySerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(slug_field="name", queryset=City.objects.all())

    class Meta:
        model = Library
        fields = ["id", "name", "city"]
        read_only_fields = ["id"]
