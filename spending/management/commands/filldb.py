from django.core.management import BaseCommand
from loguru import logger

from spending.models import ProjectSettings, SpendingCategory


class Command(BaseCommand):
    """
    Команда для наполнения БД стандартными значениями.
    """
    def handle(self, *args, **options):
        logger.info(f'Старт команды по наполнению БД стандартными настройками.')

        # Данные для таблицы ProjectSettings
        proj_settings_data = (
            ('bot_admin', '1978587604'),
            ('bot_admin', '1196122460'),
        )
        for i_key, i_value in proj_settings_data:
            i_obj, created = ProjectSettings.objects.get_or_create(
                key=i_key, value=i_value,
                defaults={
                    'key': i_key,
                    'value': i_value,
                }
            )
            logger.success(f'Запись в таблице ProjectSettings с key={i_key} value={i_value}'
                           f'{"была создана" if created else "уже есть"}.')

        # Данные для таблицы SpendingCategory
        spend_category_data = (
            '🚍 транспорт/поездки',
            '🥔 продукты',
            '🍕 ништяки (еда/вода)',
            '🪀 безделушки (чехол на телефон и т.п.)',
            '🍽️ кафешки, рестики',
            '🛍️ одежда, обувь, сумки',
            '🧴 бытовая химия и гигиена',
            '💊 аптека',
            '🩺 здоровье (например приём врача)',
            '💇 уход за собой',
            '🍿 развлечения (кино,вино,домино)',
            '📚 образование (курсы, книжки)',
            '📡 связь, интернет',
            '🚰 коммуналка',
            '🐶 питомцы',
            '💵 кредиты/долги',
            '🚗 обслуживание авто',
            '🛋️ мебель, бытовая техника',
            '🔨 ремонт хаты (обои, розетки, сантехника и т.п.)',
            '📝 другое',
        )
        for i_cat in spend_category_data:
            i_obj, created = SpendingCategory.objects.get_or_create(
                name=i_cat,
                defaults={
                    'name': i_cat,
                }
            )
            logger.success(f'Запись в таблице SpendingCategory с name={i_cat} '
                           f'{"была создана" if created else "уже есть"}.')
        logger.info(f'Команда по установке дефолтных значений в БД закончила свою работу!')
