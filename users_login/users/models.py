# -*- coding:utf8 -*-

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    mobile = models.CharField(max_length=11, verbose_name=u'手机', blank=True)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=20, choices=(('register',u'注册'),('forget',u'找回密码')), verbose_name=u'验证类型')
    send_time = models.DateTimeField(max_length=20, default=datetime.now, verbose_name=u'发送时间')

    class Meta:
        verbose_name = u'邮箱验证'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email

