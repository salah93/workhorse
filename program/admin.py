from django.contrib import admin

from .models import Day, Exercise, Info


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    fields = ["name", ("weeks", "days_per_week"), "description"]
    list_display = ["name"]


class ExerciseInline(admin.TabularInline):
    model = Exercise


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    inlines = [ExerciseInline]
