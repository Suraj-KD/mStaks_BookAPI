# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-30 17:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20190727_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='released',
            field=models.DateField(default=datetime.datetime(2019, 7, 30, 17, 45, 2, 397775, tzinfo=utc)),
        ),
    ]
