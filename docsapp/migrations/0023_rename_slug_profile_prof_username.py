# Generated by Django 4.2.5 on 2023-11-01 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docsapp', '0022_remove_editable_restricted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='slug',
            new_name='prof_username',
        ),
    ]