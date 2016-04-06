# -*- coding: utf-8 -*-
from django.forms import ModelForm
from app.models import UserRequest
from simplemathcaptcha.fields import MathCaptchaField


class UserRequestForm(ModelForm):
    captcha = MathCaptchaField()

    class Meta:
        model = UserRequest
        fields = '__all__'
        exclude = ('timestamp', 'cart',)
