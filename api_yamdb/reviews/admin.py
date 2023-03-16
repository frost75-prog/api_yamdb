from django.contrib import admin

from .models import Categories, Genres, Titles, Review, Comment

admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Titles)
admin.site.register(Review)
admin.site.register(Comment)
