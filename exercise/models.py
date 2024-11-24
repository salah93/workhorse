from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"


class BodyPart(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"


class Info(models.Model):
    name = models.CharField(max_length=30, unique=True)
    body_part = models.ForeignKey(BodyPart, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    image = models.ImageField(upload_to="exercises", null=True, blank=True)

    class Meta:
        verbose_name = "Exercise"

    def __str__(self):
        return f"{self.name}"
