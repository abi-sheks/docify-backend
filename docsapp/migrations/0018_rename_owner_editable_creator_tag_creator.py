# Generated by Django 4.2.5 on 2023-10-08 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docsapp', '0017_alter_editable_owner_alter_editable_read_tags_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='editable',
            old_name='owner',
            new_name='creator',
        ),
        migrations.AddField(
            model_name='tag',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='docsapp.profile'),
        ),
    ]