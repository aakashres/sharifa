# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20161120_1833'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemcategory',
            options={'verbose_name': 'Item category', 'verbose_name_plural': 'Item categories'},
        ),
        migrations.AddField(
            model_name='membership',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]