# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-05 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyse', '0003_auto_20171205_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datamodel',
            name='Net_Paid_Amt',
            field=models.CharField(db_column='Net Paid Amt', max_length=10),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='Pkg_Rate',
            field=models.CharField(db_column='Pkg Rate', max_length=10),
        ),
    ]
