# Generated by Django 4.2.5 on 2023-11-03 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docsapp', '0023_rename_slug_profile_prof_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='admins',
            field=models.ManyToManyField(blank=True, related_name='admintags', to='docsapp.profile'),
        ),
    ]
