from rest_framework import serializers


class StartBotSerializer(serializers.Serializer):
    """
    Сериалайзер для обработки запроса, который прилетает при старте бота.
    """
    tlg_id = serializers.CharField(max_length=30)
    tlg_username = serializers.CharField(max_length=50)
    telephone = serializers.CharField(max_length=15)
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
