# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-20 12:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20161120_1829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotation',
            name='description',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='link',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='title',
        ),
    ]
