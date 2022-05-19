from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from django.core.mail import send_mail

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        print(user.email)

        if user.email:

            send_mail(
                subject=f'Регистрация на портале Новостей',
                message=f'Добрый день!! \n Пользователь {user.username} \n зарегистрировался на портале в {datetime.utcnow()}',
                from_email='Skill.testing@yandex.ru',
                recipient_list=[user.email]
            )

        return user
