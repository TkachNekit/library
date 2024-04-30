from rest_framework import serializers

from archive.serializers import LibrarySerializer
from books.models import Book, BookCopy, Author, BookLanguage, BookGenre


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'full_name']
        read_only_fields = ['id']


class BookLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLanguage
        fields = ['id', 'name']
        read_only_fields = ['id']


class BookGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookGenre
        fields = ['id', 'name']
        read_only_fields = ['id']


class BookSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field="name", queryset=BookGenre.objects.all())
    language = serializers.SlugRelatedField(slug_field="name", queryset=BookLanguage.objects.all())
    authors = serializers.SlugRelatedField(slug_field="full_name", many=True, queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = ['id', 'title', 'genre', 'language', 'publication_date', 'description',
                  'number_of_pages', 'rating', 'cover', 'authors']
        read_only_fields = ['id']


class BookCopySerializer(serializers.ModelSerializer):
    book = BookSerializer()
    library = LibrarySerializer()

    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'library']
        read_only_fields = ['id']
