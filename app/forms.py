# -*- coding: utf-8 -*-
from django.forms import EmailInput, ModelForm
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from app.models import Subscriber, UserRequest


class UserRequestForm(ModelForm):
    # captcha = ReCaptchaField(widget=ReCaptchaWidget())

    class Meta:
        model = UserRequest
        fields = '__all__'
        exclude = ('timestamp', 'cart', 'email_is_sent', 'error_message',)


class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ('email',)
        widgets = {
            'email': EmailInput(attrs={'placeholder': 'Ваш e-mail'})
        }
