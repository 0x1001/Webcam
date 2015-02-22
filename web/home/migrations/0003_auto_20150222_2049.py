# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20150222_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='height',
            field=models.IntegerField(default=600),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='configuration',
            name='hflip',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='configuration',
            name='width',
            field=models.IntegerField(default=800),
            preserve_default=True,
        ),
    ]
