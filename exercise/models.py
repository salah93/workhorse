from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)


class BodyPart(models.Model):
    name = models.CharField(max_length=50)


class Info(models.Model):
    name = models.CharField(max_length=30)
    body_part = models.ForeignKey(BodyPart, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    image = models.ImageField(upload_to="exercises")
