from rest_framework import serializers


class StartBotSerializer(serializers.Serializer):
    """
    Сериалайзер для обработки запроса, который прилетает при старте бота.
    """
    tlg_id = serializers.CharField(max_length=30)
    tlg_username = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    language_code = serializers.CharField(max_length=10)
    api_token = serializers.CharField(max_length=46)


class GetSettingsSerializer(serializers.Serializer):
    """
    Сериалайзер для обработки запроса получения настроект
    """
    api_token = serializers.CharField(max_length=46)
    key = serializers.CharField(max_length=51)


class GetDaySpendingSerializer(serializers.Serializer):
    """
    Сериалайзер для модели трат (Spending), необходим для ответа на запрос данных из бота.
    """
    bot_user = serializers.CharField(max_length=30)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=500)
    created_at = serializers.DateTimeField()