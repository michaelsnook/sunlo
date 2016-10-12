# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 05:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_card_see_also'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='languages',
            field=models.ManyToManyField(to='cards.Language'),
        ),
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]