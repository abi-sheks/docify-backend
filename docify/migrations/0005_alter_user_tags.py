# Generated by Django 4.2.5 on 2023-09-29 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docsapp', '0004_editable_slug_alter_comment_parent_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tags',
            field=models.ManyToManyField(related_name='users', to='docsapp.tag'),
        ),
    ]
