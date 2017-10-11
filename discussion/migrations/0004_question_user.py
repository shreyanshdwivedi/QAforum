# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-13 11:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0003_question_is_answered'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='discussion.User'),
        ),
    ]
