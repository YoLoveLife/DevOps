# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 09:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('remark', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='localhost', max_length=50)),
                ('sship', models.CharField(default='192.168.1.1', max_length=15)),
                ('sshpasswd', models.CharField(default='000000', max_length=100)),
                ('sshport', models.CharField(default='22', max_length=5)),
                ('group', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='manager.Group')),
            ],
        ),
    ]