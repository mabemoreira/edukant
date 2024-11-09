# Generated by Django 5.1.3 on 2024-11-09 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("src", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Domain",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.CharField(blank=True, max_length=255)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("updated_by", models.CharField(blank=True, max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=255)),
                ("relationship", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
