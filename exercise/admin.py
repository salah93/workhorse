from django.contrib import admin

from .models import BodyPart, Category, Info


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["category__name", "body_part__name"]


admin.site.register(BodyPart)
admin.site.register(Category)
