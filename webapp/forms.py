from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from webapp.models import Order, Services, Auto, Mark, AutoModel, Reviews


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
    datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"class": "outline-none border-b p-2 w-full",
                                                                     'required': 'true', 'type': 'datetime-local'}),
                                   label='Дата и время записи')

    service = forms.ModelMultipleChoiceField(queryset=Services.objects.all(),
                                             widget=forms.CheckboxSelectMultiple(attrs={'class': 'text-slate-600'}),
                                             label='Услуги')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['auto'].queryset = Auto.objects.filter(user=user)

        self.fields['auto'].empty_label = "--Добавте автомобиль--"
        self.fields["auto"].widget.attrs.update({"class": "outline-none border-b p-2 w-full"})
        self.fields["comment"].widget.attrs.update({"class": "outline-none border-b p-2 w-full"})

    class Meta:
        model = Order
        fields = ['auto', 'service', 'datetime', 'comment']


class OrderFormAnon(forms.ModelForm):
    datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"class": "outline-none border-b p-2 w-full",
                                                                     'required': 'true', 'type': 'datetime-local'}),
                                   label='Дата и время записи')

    service = forms.ModelMultipleChoiceField(queryset=Services.objects.all(),
                                             widget=forms.CheckboxSelectMultiple(attrs={'class': 'text-slate-600'}),
                                             label='Услуги')

    mark = forms.ModelChoiceField(queryset=Mark.objects.all(), empty_label="Выберите марку", label='Марка',
                                  required=True,
                                  widget=forms.Select(attrs={"class": "outline-none border-b p-2 w-full"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'mark' in self.data:
            try:
                mark_id = int(self.data.get('mark'))
                self.fields['car_model'] = forms.ModelChoiceField(queryset=AutoModel.objects.filter(mark_id=mark_id),
                                                                  label='Модель', empty_label="Выберите модель",
                                                                  required=True,
                                                                  widget=forms.Select(attrs={'class': 'outline-none border-b p-2 w-full'}))
            except (ValueError, TypeError):
                pass
        else:
            self.fields['car_model'] = forms.ModelChoiceField(queryset=AutoModel.objects.none(), label='Модель',
                                                              empty_label="Сначала выберите марку", required=True,
                                                              widget=forms.Select(attrs={'class': 'outline-none border-b p-2 w-full'}))

        self.fields["fio"].widget.attrs.update({"class": "outline-none border-b p-2 w-full"})
        self.fields["phone"].widget.attrs.update({"class": "outline-none border-b p-2 w-full"})
        self.fields["gos_num"].widget.attrs.update({"class": "outline-none border-b p-2 w-full"})
        self.fields["comment"].widget.attrs.update({"class": "outline-none border-b p-2 w-full"})

    class Meta:
        model = Order
        fields = ['fio', 'phone', 'mark', 'car_model', 'gos_num', 'service', 'datetime', 'comment']

    def clean(self):
        cleaned_data = super().clean()
        car_model = cleaned_data.get('car_model')

        if not car_model:
            raise forms.ValidationError("Выберите модель автомобиля")

        return cleaned_data


class AutoForm(forms.ModelForm):
    mark = forms.ModelChoiceField(queryset=Mark.objects.all(), empty_label="Выберите марку", required=True,
                                  widget=forms.Select(attrs={"class": "outline-none border-b p-2 w-full", "id": "id_mark"}))

    model = forms.ModelChoiceField(queryset=AutoModel.objects.none(), empty_label="Сначала выберите марку", required=True,
                                   widget=forms.Select(attrs={"class": "outline-none border-b p-2 w-full", "id": "id_model"}))

    class Meta:
        model = Auto
        fields = ['mark', 'model', 'gos_num', 'vin_num', 'engine_num', 'released_year']
        widgets = {
            'gos_num': forms.TextInput(attrs={"class": "outline-none border-b p-2 w-full"}),
            'vin_num': forms.TextInput(attrs={"class": "outline-none border-b p-2 w-full"}),
            'engine_num': forms.TextInput(attrs={"class": "outline-none border-b p-2 w-full"}),
            'released_year': forms.NumberInput(attrs={"class": "outline-none border-b p-2 w-full"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'mark' in self.data:
            try:
                mark_id = int(self.data.get('mark'))
                self.fields['model'].queryset = AutoModel.objects.filter(mark_id=mark_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.mark_model:
            self.fields['model'].queryset = AutoModel.objects.filter(mark=self.instance.mark_model.mark)

    def clean(self):
        cleaned_data = super().clean()
        model = cleaned_data.get('model')

        if not model:
            raise forms.ValidationError("Пожалуйста, выберите модель автомобиля")

        cleaned_data['mark_model'] = model
        return cleaned_data

    def save(self, commit=True):
        auto = super().save(commit=False)
        auto.mark_model = self.cleaned_data['model']
        if commit:
            auto.save()
        return auto


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['text']

