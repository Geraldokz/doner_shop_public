from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

from .models import OrdersStatistics


class StatisticsView(LoginRequiredMixin, AccessMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.info(self.request, 'У вас не хватает прав :(')
            return redirect('mainapp:menu_page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        if OrdersStatistics.objects.filter().exists():
            model = OrdersStatistics.objects.get()
            context = {
                'orders': model
            }
            return render(self.request, 'orderstat/statistics.html', context)
        else:
            messages.info(self.request, 'Заказов не сущетсвует')
            return redirect('mainapp:menu_page')

