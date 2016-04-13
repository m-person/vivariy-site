# -*- coding: utf-8 -*-
from django.forms import ModelForm
from app.models import UserRequest
from simplemathcaptcha.fields import MathCaptchaField
from simplemathcaptcha.widgets import MathCaptchaWidget


class UserRequestForm(ModelForm):
    captcha_widget = MathCaptchaWidget(question_tmpl="Сколько будет %(num1)i %(operator)s %(num2)i?")
    captcha = MathCaptchaField(
        widget=captcha_widget,
        error_messages={
            'invalid': 'Неправильный ответ, попробуйте еще.',
            'invalid_number': 'Введите целое число.',
        }
    )

    class Meta:
        model = UserRequest
        fields = '__all__'
        exclude = ('timestamp', 'cart',)
