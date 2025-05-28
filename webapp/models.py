from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    fio = models.CharField(max_length=200, verbose_name='ФИО')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    def __str__(self):
        return self.fio


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True)
    text = models.CharField(max_length=500)
    datetime = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.text[:40]} {self.datetime}'


class Mark(models.Model):
    mark = models.CharField(max_length=100, verbose_name='Марка')
    logo = models.ImageField(upload_to='logo_auto', verbose_name='Логотип')

    def __str__(self):
        return self.mark


class AutoModel(models.Model):
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, verbose_name='Марка')
    model = models.CharField(max_length=100, verbose_name='Модель')

    def __str__(self):
        return f'{self.mark} {self.model}'


class Auto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    mark_model = models.ForeignKey(AutoModel, on_delete=models.CASCADE, verbose_name='Марка и модель')
    gos_num = models.CharField(max_length=9, verbose_name='Гос. номер', unique=True)
    vin_num = models.CharField(max_length=17, verbose_name='VIN номер', unique=True)
    engine_num = models.CharField(max_length=50, verbose_name='Серия двигателя')
    released_year = models.IntegerField(max_length=4, verbose_name='Год изготовления')

    def __str__(self):
        return f'{self.mark_model.__str__()}'


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')

    class Meta:
        verbose_name = 'Категория услуг'
        verbose_name_plural = 'Категории услуг'
        ordering = ['order']

    def __str__(self):
        return self.name


class Services(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services',
                                 verbose_name='Категория')
    name = models.CharField(max_length=150, verbose_name='Наименование')
    price = models.FloatField(verbose_name='Цена')

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = [
        ('0', 'Новая'),
        ('1', 'Ожидание'),
        ('2', 'Согласование'),
        ('3', 'В работе'),
        ('4', 'Готово'),
        ('5', 'Выдано'),
        ('6', 'Отменена')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, verbose_name='Автомобиль', null=True, blank=True)
    fio = models.CharField(max_length=200, verbose_name='ФИО', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, verbose_name='Марка', null=True, blank=True)
    car_model = models.ForeignKey(AutoModel, on_delete=models.CASCADE, verbose_name='Модель', null=True, blank=True)
    gos_num = models.CharField(max_length=9, verbose_name='Гос. номер', null=True, blank=True)
    service = models.ManyToManyField(Services, verbose_name='Услуга')
    datetime = models.DateTimeField(verbose_name='Дата и время записи')
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name='Комментарий')
    info = models.CharField(max_length=200, null=True, blank=True, verbose_name='Доп. информация')
    worker = models.CharField(max_length=200, verbose_name='Работник', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заявки')
    status = models.CharField(max_length=1, choices=STATUS, default='0', verbose_name='Статус')
    reason = models.CharField(max_length=200, null=True, blank=True, verbose_name='Причина отмены')

    def __str__(self):
        if self.user:
            user_profile = UserProfile.objects.get(user=self.user)
            return f'{user_profile.fio} {self.auto}'
        return f'{self.fio} {self.mark} {self.car_model} {self.gos_num}'

