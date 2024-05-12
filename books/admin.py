from django.contrib import admin

from books.models import Author, Book, BookCopy, BookGenre, BookLanguage

# Register your models here.
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Author)
admin.site.register(BookLanguage)
admin.site.register(BookGenre)
