# Generated by Django 4.2.5 on 2023-10-17 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docsapp', '0020_alter_editable_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editable',
            name='content',
            field=models.BinaryField(editable=True),
        ),
    ]
