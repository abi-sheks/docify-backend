# Generated by Django 4.2.5 on 2023-10-07 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docsapp', '0016_remove_editable_creation_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editable',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='docsapp.profile'),
        ),
        migrations.AlterField(
            model_name='editable',
            name='read_tags',
            field=models.ManyToManyField(blank=True, related_name='readable', to='docsapp.tag'),
        ),
        migrations.AlterField(
            model_name='editable',
            name='write_tags',
            field=models.ManyToManyField(blank=True, related_name='writeable', to='docsapp.tag'),
        ),
    ]
