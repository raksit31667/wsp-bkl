# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-24 08:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0010_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('net', models.PositiveSmallIntegerField(default=0)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='cost',
            new_name='price',
        ),
    ]
