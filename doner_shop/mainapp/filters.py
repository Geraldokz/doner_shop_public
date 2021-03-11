import django_filters
from django_filters import DateFilter

from .models import Order


class OrdersFilter(django_filters.FilterSet):
    date = DateFilter(field_name='ordered_date', lookup_expr='date')

    class Meta:
        model = Order
        fields = ['ordered_date']
