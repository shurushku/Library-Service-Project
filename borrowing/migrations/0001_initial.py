from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrowing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("borrow_date", models.DateField(auto_now_add=True)),
                ("expected_return_date", models.DateField()),
                ("actual_return_date", models.DateField(blank=True, null=True)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            name='Borrowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField(auto_created=True)),
                ('actual_return_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
