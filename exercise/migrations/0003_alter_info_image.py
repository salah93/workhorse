# Generated by Django 5.1.3 on 2024-11-24 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exercise", "0002_alter_info_options_alter_bodypart_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="info",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="exercises"
            ),
        ),
    ]
