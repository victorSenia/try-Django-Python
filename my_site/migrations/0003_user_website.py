# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0002_auto_20161025_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='website',
            field=models.URLField(blank=True),
        ),
    ]