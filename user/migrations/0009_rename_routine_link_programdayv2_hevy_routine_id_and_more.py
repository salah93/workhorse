# Generated by Django 5.1.3 on 2024-12-02 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0008_program_hevy_routine_folder_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="programdayv2",
            old_name="routine_link",
            new_name="hevy_routine_id",
        ),
        migrations.AlterField(
            model_name="program",
            name="hevy_routine_folder_id",
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
