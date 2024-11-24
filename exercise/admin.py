from django.contrib import admin

from .models import BodyPart, Category, Info

admin.site.register(BodyPart)
admin.site.register(Category)
admin.site.register(Info)
