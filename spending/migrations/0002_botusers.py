# Generated by Django 4.2.1 on 2023-06-04 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spending', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tlg_id', models.CharField(max_length=30, verbose_name='TG ID')),
                ('tlg_username', models.CharField(max_length=50, null=True, verbose_name='TG username')),
                ('telephone', models.CharField(max_length=15, null=True, verbose_name='телефон')),
                ('first_name', models.CharField(max_length=100, null=True, verbose_name='имя')),
                ('last_name', models.CharField(max_length=100, null=True, verbose_name='фамилия')),
                ('start_at', models.DateTimeField(auto_now_add=True, verbose_name='дата старта бота')),
                ('language_code', models.CharField(max_length=100, null=True, verbose_name='язык')),
            ],
            options={
                'verbose_name': 'юзер spending бота',
                'verbose_name_plural': 'юзеры spending бота',
                'ordering': ['-id'],
            },
        ),
    ]
