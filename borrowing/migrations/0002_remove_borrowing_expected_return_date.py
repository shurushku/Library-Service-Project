# Generated by Django 4.1.3 on 2022-11-29 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("borrowing", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="borrowing",
            name="expected_return_date",
        ),
    ]