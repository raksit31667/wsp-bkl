# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-14 03:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_auto_20161014_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_name',
            field=models.CharField(default='Movie Name', max_length=300),
        ),
    ]
