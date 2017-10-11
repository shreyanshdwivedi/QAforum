# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-13 12:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0008_auto_20170813_1732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='user_id',
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='discussion.User'),
        ),
    ]
