from django.core.management import BaseCommand
from loguru import logger
from datetime import datetime, timedelta
from spending.models import Spending


class Command(BaseCommand):
    """
    Команда для изменения даты и времени записи, относительно N кол-во дней от текущей даты.
    """
    def handle(self, *args, **options):
        logger.info(f'Старт команды для изменения даты и времени записи.')
        pk_lst = [2271, 2272, 2273, 2274, 2275]
        today = datetime.today()
        spendings_today = Spending.objects.filter(pk__in=pk_lst)
        spendings_today.update(created_at=today)