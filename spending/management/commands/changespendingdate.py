from django.core.management import BaseCommand
from loguru import logger
from datetime import datetime, timedelta
from spending.models import ProjectSettings, SpendingCategory, Spending


class Command(BaseCommand):
    """
    Команда для изменения даты и времени записи, относительно N кол-во дней от текущей даты.
    """
    def handle(self, *args, **options):
        logger.info(f'Старт команды для изменения даты и времени записи.')

        today = datetime.today()
        yesterday = today - timedelta(days=1)
        spendings_today = Spending.objects.filter(created_at__date=today)
        spendings_today.update(created_at=yesterday)