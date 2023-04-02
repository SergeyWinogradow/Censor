from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, News


admin.site.register(Author)
admin.site.register(News)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
