# Generated by Django 4.1.7 on 2024-08-28 00:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_utilisateurs_photo"),
    ]

    operations = [
        migrations.AddField(
            model_name="utilisateurs",
            name="phone_number",
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
