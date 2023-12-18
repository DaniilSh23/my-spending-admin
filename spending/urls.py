from django.urls import path

from spending.views import StartBotView, GetSettingsView, WriteSpendingView, test_view, GetDaySpending, \
    GetMonthSpending, AverageAmountSpent

app_name = 'spending'

urlpatterns = [
    path('start_bot/', StartBotView.as_view(), name='start_bot'),
    path('get_settings/', GetSettingsView.as_view(), name='get_settings'),
    path('write_spending/', WriteSpendingView.as_view(), name='write_spending'),
    path('get_day_spending/', GetDaySpending.as_view(), name='get_day_spending'),
    path('get_month_spending/', GetMonthSpending.as_view(), name='get_month_spending'),
    path('average_amount_spent/', AverageAmountSpent.as_view(), name='average_amount_spent'),

    path('test/', test_view, name='test'),
]