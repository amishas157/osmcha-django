# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-28 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changeset', '0039_auto_20170301_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suspicionreasons',
            name='name',
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
    ]
