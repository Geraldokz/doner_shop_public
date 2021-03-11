from django.urls import path

from .views import (
    StatisticsView,
    # stat
)

app_name = 'orderstat'

urlpatterns = [
    path('', StatisticsView.as_view(), name='statistics'),
]