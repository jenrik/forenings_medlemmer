# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-07-19 10:40
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0097_auto_20170612_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='unique',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
