# Generated by Django 1.9.1 on 2016-04-28 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0070_auto_20160322_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='approved',
            field=models.BooleanField(default=True, verbose_name='Godkendt af afdelingsleder'),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='removed',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Slut'),
        ),
        migrations.AlterField(
            model_name='person',
            name='membertype',
            field=models.CharField(choices=[('PA', 'Forælder'), ('GU', 'Værge'), ('CH', 'Barn'), ('NA', 'Anden')], default='PA', max_length=2, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='added',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Start'),
        ),
    ]
