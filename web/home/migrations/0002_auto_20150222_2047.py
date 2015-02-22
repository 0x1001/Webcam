# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='hflip',
            field=models.BooleanField(verbose_name=False),
            preserve_default=True,
        ),
    ]
