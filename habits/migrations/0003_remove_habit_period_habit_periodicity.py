# Generated by Django 5.0.7 on 2024-07-21 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0002_remove_habit_duration_habit_owner_habit_period_time_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="habit",
            name="period",
        ),
        migrations.AddField(
            model_name="habit",
            name="periodicity",
            field=models.PositiveIntegerField(
                default=7,
                help_text="Укажите периодичность выполнения привычки",
                verbose_name="Периодичность",
            ),
        ),
    ]
