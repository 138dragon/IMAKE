# Generated by Django 3.0.6 on 2020-05-27 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_article_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='email',
        ),
        migrations.RemoveField(
            model_name='article',
            name='url',
        ),
    ]
