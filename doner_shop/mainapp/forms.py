from django import forms


class CheckoutForm(forms.Form):

    ORDER_CHOICES = (
        ('Shop', 'На месте'),
        ('Delivery', 'Доставка'),
        ('Stuff', 'Персонал'),
    )

    PAYMENT_CHOICES = (
        ('Cash', 'Наличный'),
        ('Card', 'Безналичный'),
    )

    DELIVERY_CHOICES = (
        ('Delivery', 'Delivery Club'),
        ('Yandex', 'Яндекс.Еда'),
    )

    order_type = forms.ChoiceField(widget=forms.Select, choices=ORDER_CHOICES)
    payment_type = forms.ChoiceField(widget=forms.Select, choices=PAYMENT_CHOICES, required=False)
    delivery_name = forms.ChoiceField(widget=forms.Select, choices=DELIVERY_CHOICES, required=False)


class CouponForm(forms.Form):
    code = forms.CharField(required=False, label='Промокод')


