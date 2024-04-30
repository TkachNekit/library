from rest_framework import serializers

from archive.models import Library, City


class LibrarySerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(slug_field="name", queryset=City.objects.all())

    class Meta:
        model = Library
        fields = ['id', 'name', 'city']
        read_only_fields = ['id']
