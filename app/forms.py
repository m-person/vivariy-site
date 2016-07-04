# -*- coding: utf-8 -*-
from django.forms import ModelForm, EmailInput
from app.models import UserRequest, Subscriber
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
        exclude = ('timestamp', 'cart', 'email_is_sent', 'error_message', )


class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ('email',)
        widgets = {
            'email': EmailInput(attrs={'placeholder': 'Ваш e-mail'})
        }
