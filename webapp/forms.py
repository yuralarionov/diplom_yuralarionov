from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from webapp.models import Order, Auto


class RegisterForm(UserCreationForm):
    fio = forms.CharField(widget=forms.TextInput(attrs={"class": "peer border-b outline-none text-xl w-full",
                                                        'required': 'true', "placeholder": "ФИО"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "peer border-b outline-none text-xl w-full",
                                                          'required': 'true', "placeholder": "Телефон"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "peer border-b outline-none text-xl w-full",
                                                     "placeholder": "Логин"})
        self.fields["password1"].widget.attrs.update({"class": "peer border-b outline-none text-xl w-full",
                                                      "placeholder": "Пароль"})
        self.fields["password2"].widget.attrs.update({"class": "peer border-b outline-none text-xl w-full",
                                                      "placeholder": "Потверждение пароля"})
        self.fields["email"].widget.attrs.update({"class": "peer border-b outline-none text-xl w-full",
                                                  "placeholder": "E-mail"})

    class Meta:
        model = User
        fields = ["fio", "username", "password1", "password2", "phone", "email"]

class OrderForm(forms.ModelForm):
    datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
                                    "class": "peer border-b outline-none text-xl w-full", 'required': 'true',
                                    'type': 'datetime-local'}),
                                   label='Дата и время записи')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["auto"].widget.attrs.update({"class": "peer border-b outline-none text-xl w-full"})
        self.fields["service"].widget.attrs.update({"class": "peer border-b outline-none text-xl w-full"})
        self.fields["datetime"].widget.attrs.update({"class": "peer border-b outline-none text-xl w-full"})
        self.fields["comment"].widget.attrs.update({"class": "peer border-b outline-none text-xl w-full"})
        self.fields["info"].widget.attrs.update({"class": "peer border-b outline-none text-xl w-full"})

    class Meta:
        model = Order
        fields = ['auto', 'service', 'datetime', 'comment', 'info']
