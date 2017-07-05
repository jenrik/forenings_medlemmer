# Generated by Django 1.9.1 on 2016-07-10 20:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0071_auto_20160710_0100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='union',
            options={'ordering': ['name'], 'verbose_name': 'Forening', 'verbose_name_plural': 'Foreninger'},
        ),
        migrations.AlterField(
            model_name='department',
            name='union',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Union', verbose_name='Lokalforening'),
        ),
    ]
