# -*- coding:utf8 -*-
import random,string

from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from .forms import LoginForm, RegisterEmailForm
from .models import UserProfile, EmailVerifyRecord
from users_login.settings import EMAIL_FROM
# Create your views here.


# 生成随机字符串
def random_str(str_length=16):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:str_length])


# 验证邮箱发送
def send_register_email(email, send_type='register'):
    # 数据库操作
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code=code
    email_record.email=email
    email_record.send_type=send_type
    email_record.save()

    # 发送邮件
    if send_type=='register':
        email_title = '注册激活链接'
        email_body = '点击激活帐并登录：http://127.0.0.1:8000/user/active/{0}'.format(code)

        email_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if email_status:
            pass


# 邮箱注册
class RegisterEmailView(View):
    def get(self, request):
        register_email_form = RegisterEmailForm()
        return render(request, 'register_mail.html', {'register_email_form': register_email_form})

    def post(self, request):
        register_email_form = RegisterEmailForm(request.POST)
        login_form = LoginForm()
        if register_email_form.is_valid():
            username = request.POST.get('username', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return render(request, 'register_mail.html', {'msg': u'密码不一致', 'register_email_form':register_email_form})
            if UserProfile.objects.filter(email=username):
                return render(request, 'login.html',{'msg': '邮箱已注册', 'login_form': login_form})
            # 数据操作
            userprofile = UserProfile()
            userprofile.username = username
            userprofile.email = username
            userprofile.password = make_password(password1)
            userprofile.is_active = False
            userprofile.save()
            # 邮件发送
            send_register_email(email=username, send_type='register')
            return render(request, 'login.html', {'msg': u'请激活后登录', 'login_form': login_form })
        else:
            return render(request, 'register_mail.html', {'register_email_form': register_email_form})


# 邮件激活
class EmailActiveView(View):
    def get(self, request, active_code):
        login_form = LoginForm()
        records = EmailVerifyRecord.objects.filter(code=active_code)
        if records:  # 默认记录会有不知数量条(防止验证码可能重复)
            for record in records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html', {})
        return render(request, 'login.html', {'login_form': login_form, 'msg': '激活成功'})


# 登录
class LoginView(View):

    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form':login_form}) # 返回form主要是为提取验证码表单验证

    def post(self, request):
        login_form = LoginForm(request.POST)
        # form验证是否正确
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            # 如果用户是否存在
            if user is not None:
                # 用户是否激活
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return request(request, 'login.html', {'msg': u'用户未激活','login_form': login_form})
            else:
                return render(request, 'login.html', {'msg': u'密码错误或用户不存在','login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 登出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request,'index.html', {})
