# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-05 06:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20180220_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='biography',
            name='death_of_death',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Death of death'),
        ),
        migrations.AddField(
            model_name='biography',
            name='place_of_death',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Place of death'),
        ),
    ]