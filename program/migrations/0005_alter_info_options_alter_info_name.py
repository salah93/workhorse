# Generated by Django 5.1.3 on 2024-11-24 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("program", "0004_exercise"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="info",
            options={"verbose_name": "Program"},
        ),
        migrations.AlterField(
            model_name="info",
            name="name",
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
