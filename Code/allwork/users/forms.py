#！/usr/bin/env.python
# _*_ coding:utf-8 _*_

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import transaction
from .models import User

class UserCreationForm(forms.ModelForm):
    """创建用户的表单"""
    username = forms.CharField(max_length=30,required=True,help_text='Required.')
    first_name = forms.CharField(max_length=30,required=True,help_text='Optional.')
    last_name = forms.CharField(max_length=30,required=True,help_text='Optional.')
    email = forms.EmailField(max_length=254,required=True,help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.charField(label='Password Confirmation',widget=forms.PasswordInput) # 确认密码

    class Meta:
        #注册表单字段
        model = User
        fields = ('username','first_name','last_name','email','password1','password2',)

    def clean_password(self):
        #检查两次密码是否相同
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self,commit=True):
        #以哈希格式存储密码
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(form.ModelForm):
    """用于更新用户的表单。包括用户的所有字段，但用admin的密码哈希显示字段替换密码字段。"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','password','first_name','last_name','username','is_active','is_admin')

    def clean_password(self):
        #无论用户提供什么，都要返回初始值。
        #这是在这里完成的，而不是在现场，因为field无权访问初始值。
        return self.initial['password']


#自由职业者的创建表单
class FreelancerSignUpForm(UserCreationForm):
    @transaction.atomic
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_freelancer = True
        user.save()
        return user

#客户的创建表单
class OwnerSignUpForm(UserCreationForm):
    @transaction.atomic
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_owner = True
        if commit:
            user.save()
        return user