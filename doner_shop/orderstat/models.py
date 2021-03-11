from django.db import models


class OrdersStatistics(models.Model):
    date = models.DateTimeField(null=True, blank=True)
