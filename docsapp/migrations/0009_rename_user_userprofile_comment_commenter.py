# Generated by Django 4.2.5 on 2023-10-06 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docsapp', '0008_remove_tag_creator'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserProfile',
        ),
        migrations.AddField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='docsapp.userprofile'),
        ),
    ]