# Generated by Django 4.2.5 on 2023-10-06 17:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('docsapp', '0013_alter_userprofile_profile_of'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(default='', validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')])),
                ('profile_of', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(related_name='users', to='docsapp.tag')),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='docsapp.profile'),
        ),
        migrations.AlterField(
            model_name='editable',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docsapp.profile'),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]