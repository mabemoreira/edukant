# Generated by Django 5.1.3 on 2024-11-09 20:42

from django.db import migrations, models


def create_visibility_domains(apps, schema_editor):
    Domain = apps.get_model("src", "Domain")
    Domain.objects.create(
        name="public",
        type="visibility",
        relationship="StudyPlan",
        created_by="0003_visibility_domains",
    )
    Domain.objects.create(
        name="private",
        type="visibility",
        relationship="StudyPlan",
        created_by="0003_visibility_domains",
    )


def delete_visibility_domains(apps, schema_editor):
    Domain = apps.get_model("src", "Domain")
    Domain.objects.filter(created_by="0003_visibility_domains").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("src", "0001_initial"),
        ("src", "0002_domain"),
    ]

    operations = [
        migrations.RunPython(create_visibility_domains, delete_visibility_domains),
    ]
