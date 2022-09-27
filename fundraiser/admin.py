from django.contrib import admin

from .models import Category, Fundraiser, Image, Comment, Donation

admin.site.register(Category)
admin.site.register(Fundraiser)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Donation)
