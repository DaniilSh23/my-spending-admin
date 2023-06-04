from django.urls import path

from spending.views import StartBotView, GetSettingsView

app_name = 'spending'

urlpatterns = [
    path('start_bot/', StartBotView.as_view(), name='start_bot'),
    path('get_settings/', GetSettingsView.as_view(), name='get_settings'),
]