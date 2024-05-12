import django_filters
from django.db.models import Q

from books.models import Book


class BookFilter(django_filters.FilterSet):
    title_or_author = django_filters.CharFilter(
        method="my_custom_filter", label="Search name or author"
    )

    class Meta:
        model = Book
        fields = {
            "genre": ["exact"],
            "language": ["exact"],
            "number_of_pages": ["lte", "gte"],
            "rating": ["gte"],
        }

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(authors__first_name__icontains=value)
            | Q(authors__last_name__icontains=value)
            | Q(title__icontains=value)
        ).distinct()
