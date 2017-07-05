# Generated by Django 1.9.1 on 2016-10-16 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0086_auto_20161009_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='union',
            name='secretary',
            field=models.CharField(blank=True, max_length=200, verbose_name='Sekratær'),
        ),
        migrations.AlterField(
            model_name='union',
            name='cashier',
            field=models.CharField(blank=True, max_length=200, verbose_name='Kasserer'),
        ),
        migrations.AlterField(
            model_name='union',
            name='cashier_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Sekratærens email'),
        ),
    ]
