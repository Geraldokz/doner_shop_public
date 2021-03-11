from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse

from .forms import CheckoutForm

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=255, default=None, verbose_name='Наименование товара')
    price = models.FloatField(verbose_name='Цена')
    category = models.ForeignKey('Category', verbose_name='Категория товара', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=40, verbose_name='Slug товара', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Товар в продаже')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mainapp:product', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_from_product_list_url(self):
        return reverse("mainapp:add-to-cart-from-product-list", kwargs={
            'slug': self.slug
        })

    def get_remove_single_product_from_product_list_urls(self):
        return reverse("mainapp:remove-single-product-from-product-list", kwargs={
            'slug': self.slug
        })


class Category(models.Model):
    name = models.CharField(max_length=255, default=None, verbose_name='Наименование категории')
    slug = models.SlugField(max_length=40, verbose_name='Slug категории', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mainapp:category', kwargs={
            'slug': self.slug
        })


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Продавец')
    ordered = models.BooleanField(default=False, verbose_name='Товар в завершенном заказе')
    quantity = models.IntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.product.name}. Количество - {self.quantity}'

    def get_total_item_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Продавец')
    ordered = models.BooleanField(default=False, verbose_name='Заказ завершен')
    products = models.ManyToManyField(OrderProduct, verbose_name='Товары в заказе')
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(verbose_name='Время оформления заказа')
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    order_type = models.CharField(max_length=30, choices=CheckoutForm.ORDER_CHOICES, verbose_name='Тип заказа',
                                  default='Shop')
    payment_type = models.CharField(max_length=30, verbose_name='Тип оплаты', choices=CheckoutForm.PAYMENT_CHOICES,
                                    null=True, blank=True)
    delivery_name = models.CharField(max_length=30, verbose_name='Имя доставки', choices=CheckoutForm.DELIVERY_CHOICES,
                                     null=True, blank=True)
    final_price = models.FloatField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'Заказ номер {self.id}'

    def get_total_price(self):
        total_price = 0
        for order_product in self.products.all():
            total_price += order_product.get_total_item_price()
        if self.coupon:
            return total_price - (self.coupon.discount / 100 * total_price)
        else:
            return total_price

    def get_absolute_url(self):
        return reverse('mainapp:order-detail', kwargs={
            'pk': self.pk
        })


class Coupon(models.Model):
    code = models.CharField(max_length=50, verbose_name='Код купона', unique=True)
    discount = models.IntegerField(verbose_name='Скидка в процентах')
    status = models.BooleanField(verbose_name='Купон активен', default=True)

    def __str__(self):
        return f'Купон {self.code} для скидки в {self.discount}%'
