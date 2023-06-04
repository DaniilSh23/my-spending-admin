from django.shortcuts import render
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from myspending.settings import MY_LOGGER, BOT_TOKEN
from spending.models import BotUsers, ProjectSettings
from spending.serializers import StartBotSerializer, GetSettingsSerializer


class StartBotView(APIView):
    """
    Вьюшка для старта бота.
    """
    def post(self, request):
        MY_LOGGER.debug(f'Получен POST запрос в StartBotView. {request.data}')

        serializer = StartBotSerializer(data=request.data)

        if serializer.is_valid() and serializer.validated_data.get("api_token") == BOT_TOKEN:
            MY_LOGGER.debug(f'Данные запроса валидны. Обновляем или достаём из БД юзера')
            user_obj, created = BotUsers.objects.update_or_create(
                tlg_id=serializer.validated_data.get("tlg_id"),
                defaults={
                    "tlg_id": serializer.validated_data.get("tlg_id"),
                    "tlg_username": serializer.validated_data.get("tlg_username"),
                    "telephone": serializer.validated_data.get("telephone"),
                    "first_name": serializer.validated_data.get("first_name"),
                    "last_name": serializer.validated_data.get("last_name"),
                    "language_code": serializer.validated_data.get("language_code"),
                }
            )
            MY_LOGGER.debug(f'Юзер {serializer.validated_data.get("tlg_id")!r} '
                            f'был {"создан" if created else "обновлён"} в БД')
            return Response(
                data={'result': 'ok'},
                status=status.HTTP_200_OK
            )
        else:
            MY_LOGGER.debug(f'Данные не прошли валидацию. Поступивший запрос: {request.data}')
            return Response(data={"result": f'Request data was not validated. Errors: {serializer.errors}'},
                            status=status.HTTP_400_BAD_REQUEST)


class GetSettingsView(APIView):
    """
    Вьюшка для получения настроек по ключу
    """
    def post(self, request: Request):
        """
        Принимает параметр запроса key=ключ настройки. Отдаёт JSON с настройками, либо с описанием ошибки
        """
        MY_LOGGER.debug(f'Получен POST запрос для получения настроек')

        serializer = GetSettingsSerializer(data=request.data)
        if serializer.is_valid() and serializer.validated_data.get("api_token") == BOT_TOKEN:
            key = serializer.validated_data.get("key")
            bot_settings = ProjectSettings.objects.filter(key=key)
            MY_LOGGER.debug(f'Список настроек по ключу {key!r}: {bot_settings}')
            return Response(data={'result': [i_set.value for i_set in bot_settings]}, status=status.HTTP_200_OK)
        else:
            MY_LOGGER.warning(f'Значение ключа слишком длинное')
            return Response(data={'result:' 'значение ключа слишком длинное'}, status=status.HTTP_400_BAD_REQUEST)