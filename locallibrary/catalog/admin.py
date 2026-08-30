from django.contrib import admin

from .models import Book, BookInstance, Language, Genre, Author

# Register your models here.

admin.site.register(BookInstance)
admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
