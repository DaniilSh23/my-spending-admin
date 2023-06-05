from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from myspending.settings import MY_LOGGER, BOT_TOKEN
from spending.forms import NewSpendingForm
from spending.models import BotUsers, ProjectSettings, SpendingCategory, Spending
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


class WriteSpendingView(View):
    """
    Вьюшки для обработки get и post запросов при создании записи о трате
    """
    def get(self, request):
        MY_LOGGER.debug(f'Получен GET запрос для отображения формы внесения трат.')
        context = {
            'categories': SpendingCategory.objects.all(),
        }
        return render(request, template_name='spending/write_spending.html', context=context)

    def post(self, request):
        MY_LOGGER.debug(f'Получен POST запрос для записи новой траты. {request.POST}')

        form = NewSpendingForm(request.POST)
        if form.is_valid():
            MY_LOGGER.debug(f'POST запрос валиден')

            # Достаём из БД юзера по его tlg_id
            try:
                user_obj = BotUsers.objects.get(tlg_id=form.cleaned_data.get("tlg_id"))
            except ObjectDoesNotExist:
                MY_LOGGER.warning(f'Объект BotUser с tlg_id={form.cleaned_data.get("tlg_id")} не найден в БД')
                return HttpResponse(status=404)

            # Достаём из БД категорию
            try:
                category_obj = SpendingCategory.objects.get(name=form.cleaned_data.get("category"))
            except ObjectDoesNotExist:
                MY_LOGGER.warning(f'Объект SpendingCategory с name={form.cleaned_data.get("category")} не найден в БД')
                return HttpResponse(status=404)

            # Создаём новую запись отратах
            try:
                spending_obj = Spending.objects.create(
                    bot_user=user_obj,
                    amount=form.cleaned_data.get("amount"),
                    category=category_obj,
                    description=form.cleaned_data.get("description"),
                )
            except Exception as err:
                MY_LOGGER.error(f'Неожиданная ошибка при создании записи в БД о новых тратах. Вот её текст: {err}')
                return HttpResponse(status=400, content='Неверный запрос.')

            # Даём ответ в случае успешной обработки запроса
            context = {
                'amount': spending_obj.amount,
                'category': category_obj.name,
                'datetime': spending_obj.created_at,
            }
            MY_LOGGER.success(f'Запрос на запись новой траты для юзера {user_obj!r} успешно обработан!')
            return render(request, template_name='spending/success.html', context=context)

        else:
            MY_LOGGER.debug(f'POST запрос невалиден')
            context = {
                'categories': SpendingCategory.objects.all(),
                'form': form,
            }
            return render(request, template_name='spending/write_spending.html', context=context)


def test_view(request):
    return render(request, template_name='spending/success.html')
