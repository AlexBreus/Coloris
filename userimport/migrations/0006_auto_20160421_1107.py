# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 11:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userimport', '0005_auto_20160421_1106'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
    ]