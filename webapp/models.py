from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    fio = models.CharField(max_length=200, verbose_name='ФИО')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    def __str__(self):
        return self.fio


class AutoMarkModel(models.Model):
    mark = models.CharField(max_length=100, verbose_name='Марка')
    model = models.CharField(max_length=100, verbose_name='Модель')

    def __str__(self):
        return f'{self.mark} {self.model}'

class Auto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    mark_model = models.OneToOneField(AutoMarkModel, on_delete=models.CASCADE, verbose_name='Марка и модель')
    gos_num = models.CharField(max_length=9, verbose_name='Гос. номер')
    vin_num = models.CharField(max_length=17, verbose_name='VIN номер')
    engine_num = models.CharField(max_length=50, verbose_name='Серия и номер двигателя')
    released_year = models.IntegerField(max_length=4, verbose_name='Год изготовления')

    def __str__(self):
        user_profile = UserProfile.objects.get(user=self.user)
        return f'{user_profile.fio} {self.mark_model.__str__()} {self.gos_num}'

class Services(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    price = models.FloatField(verbose_name='Цена')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, verbose_name='Автомобиль')
    service = models.ManyToManyField(Services, verbose_name='Услуга')
    datetime = models.DateTimeField(verbose_name='Дата и время записи')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')
    info = models.CharField(max_length=200, null=True, blank=True, verbose_name='Доп. информация')
    worker = models.CharField(max_length=200, verbose_name='Работник')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заявки')

    def __str__(self):
        user_profile = UserProfile.objects.get(user=self.user)
        return f'{user_profile.fio}'

