# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-29 10:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('send_type', models.CharField(choices=[('register', '注册'), ('forget', '找回密码')], max_length=20, verbose_name='验证类型')),
                ('send_time', models.DateTimeField(default=datetime.datetime.now, max_length=20, verbose_name='发送时间')),
            ],
            options={
                'verbose_name': '邮箱验证',
                'verbose_name_plural': '邮箱验证',
            },
        ),
    ]
