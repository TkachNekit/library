from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from archive.models import Library


class BookGenre(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class BookLanguage(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False, unique=True)

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=128, blank=False, null=False)
    last_name = models.CharField(max_length=128, blank=True)

    class Meta:
        # Define unique together constraint for first_name and last_name
        unique_together = ['first_name', 'last_name']
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.last_name, self.first_name)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()


class RatingField(models.FloatField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [MinValueValidator(0), MaxValueValidator(10)])
        super().__init__(*args, **kwargs)


class Book(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)
    genre = models.ForeignKey(to=BookGenre, on_delete=models.CASCADE, null=False, blank=False)
    language = models.ForeignKey(to=BookLanguage, on_delete=models.CASCADE, null=False, blank=False)
    publication_date = models.DateField()
    description = models.TextField(blank=True)
    number_of_pages = models.PositiveIntegerField(null=True, blank=True)
    rating = RatingField(null=True, blank=True)
    cover = models.ImageField(upload_to='books_covers', null=True, blank=True)
    authors = models.ManyToManyField(Author, blank=False)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f"{self.title} | {self.publication_date.year} | {self.language}"


class BookCopy(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    library = models.ForeignKey(to=Library, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Экземпляр книги"
        verbose_name_plural = "Экземпляры книг"

    def __str__(self):
        return f"{self.book.title } | {self.library.name}"
