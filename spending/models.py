from django.db import models


class ProjectSettings(models.Model):
    """
    Настройки для проекта
    """
    key = models.CharField(verbose_name='Ключ', max_length=230)
    value = models.TextField(verbose_name='Значение', max_length=500)

    class Meta:
        ordering = ['-id']
        verbose_name = 'настройка проекта'
        verbose_name_plural = 'настройки проекта'


class BotUsers(models.Model):
    """
    Модель для таблицы БД, хранящей инфу о юзерах телеги
    """
    tlg_id = models.CharField(verbose_name='TG ID', max_length=30)
    tlg_username = models.CharField(verbose_name='TG username', max_length=50, blank=False, null=True)
    telephone = models.CharField(verbose_name='телефон', max_length=15, blank=False, null=True)
    first_name = models.CharField(verbose_name='имя', max_length=100, blank=False, null=True)
    last_name = models.CharField(verbose_name='фамилия', max_length=100, blank=False, null=True)
    start_at = models.DateTimeField(verbose_name='дата старта бота', auto_now_add=True)
    language_code = models.CharField(verbose_name='язык', max_length=10, blank=False, null=True)

    def __str__(self):
        return f'{self.tlg_id!r}|{self.tlg_username!r}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'юзер spending бота'
        verbose_name_plural = 'юзеры spending бота'


class SpendingCategory(models.Model):
    """
    Модель для таблицы БД с категориями трат
    """
    name = models.CharField(verbose_name='категория трат', max_length=50)

    def __str__(self):
        return f'кат. трат: {self.name!r}'

    class Meta:
        ordering = ['id']
        verbose_name = 'категория трат'
        verbose_name_plural = 'категории трат'


class Spending(models.Model):
    """
    Модель для таблицы трат.
    """
    bot_user = models.ForeignKey(verbose_name='юзер бота', to=BotUsers, on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name='сумма', max_digits=10, decimal_places=2)
    category = models.ForeignKey(verbose_name='категория', to=SpendingCategory, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='описание', max_length=500, blank=True, null=False)
    created_at = models.DateTimeField(verbose_name='дата и время', auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'трата'
        verbose_name_plural = 'траты'
