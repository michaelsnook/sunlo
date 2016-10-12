# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_auto_20161002_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardtranslation',
            name='literal',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='deck',
            name='learning',
            field=models.ManyToManyField(blank=True, to='cards.CardTranslation'),
        ),
    ]
