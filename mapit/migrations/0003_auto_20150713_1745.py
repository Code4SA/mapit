# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapit', '0002_auto_20141218_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='code',
            field=models.CharField(max_length=500, db_index=True),
        ),
        migrations.AlterUniqueTogether(
            name='code',
            unique_together=set([('area', 'type', 'code')]),
        ),
    ]
