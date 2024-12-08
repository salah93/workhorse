# Generated by Django 5.1.3 on 2024-12-03 02:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exercise", "0005_remove_bodypart_hevy_template_id_and_more"),
        (
            "user",
            "0009_rename_routine_link_programdayv2_hevy_routine_id_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile1rm",
            old_name="bench",
            new_name="weight",
        ),
        migrations.AddField(
            model_name="profile1rm",
            name="exercise",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="exercise.info",
            ),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name="profile1rm",
            unique_together={("user", "exercise")},
        ),
        migrations.AlterField(
            model_name="profile1rm",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RemoveField(
            model_name="profile1rm",
            name="deadlift",
        ),
        migrations.RemoveField(
            model_name="profile1rm",
            name="overhand_press",
        ),
        migrations.RemoveField(
            model_name="profile1rm",
            name="safety_squat_bar",
        ),
        migrations.RemoveField(
            model_name="profile1rm",
            name="squat",
        ),
    ]