# Generated by Django 1.9.1 on 2017-05-28 09:29
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0094_auto_20170527_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='union',
            name='bank_reg_number',
        ),
        migrations.AlterField(
            model_name='union',
            name='bank_account',
            field=models.CharField(blank=True, help_text='Kontonummer i formatet 1234-1234567890', max_length=15, validators=[django.core.validators.RegexValidator(message='Indtast kontonummer i det rigtige format.', regex='^[0-9]{4} *?-? *?[0-9]{6,10} *?$')], verbose_name='Bankkonto:'),
        ),
    ]
