# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-09 02:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_auto_20170108_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='type',
            field=models.PositiveIntegerField(choices=[(0, 'limited'), (1, 'silver'), (2, 'gold'), (3, 'platinum'), (4, 'vip')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.ItemCategory'),
        ),
    ]