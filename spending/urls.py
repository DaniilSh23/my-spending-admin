from django.urls import path

from spending.views import StartBotView, GetSettingsView, WriteSpendingView, test_view, GetDaySpending

app_name = 'spending'

urlpatterns = [
    path('start_bot/', StartBotView.as_view(), name='start_bot'),
    path('get_settings/', GetSettingsView.as_view(), name='get_settings'),
    path('write_spending/', WriteSpendingView.as_view(), name='write_spending'),
    path('get_day_spending/', GetDaySpending.as_view(), name='get_day_spending'),

    path('test/', test_view, name='test'),
]