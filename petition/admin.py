from django.contrib import admin

from .models import Petition, Category, Image, Comment

admin.site.register(Petition)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Comment)

