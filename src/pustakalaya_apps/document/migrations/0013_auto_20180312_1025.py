# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-12 04:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0012_auto_20180307_1007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentseries',
            options={'verbose_name_plural': 'Document series'},
        ),
    ]
