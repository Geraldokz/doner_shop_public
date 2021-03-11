from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View, DetailView
from django.utils import timezone


from .filters import OrdersFilter
from .forms import CheckoutForm, CouponForm
from .services import add_to_cart, remove_single_product, remove_product
from .models import Category, Product, OrderProduct, Order, Coupon


@login_required(login_url='/login/')
def get_menu_page(request):
    return render(request, 'mainapp/menu.html')


class CategoriesView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Category
    template_name = 'mainapp/main.html'
    context_object_name = 'categories'


class ProductsView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'mainapp/category_detail.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category, is_active=True)


class CartView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, *args, **kwargs):
        if Order.objects.filter(user=self.request.user, ordered=False).exists():
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CouponForm()
            context = {
                'object': order,
                'form': form
            }
            return render(self.request, 'mainapp/cart.html', context)
        else:
            messages.info(self.request, 'Заказа не существует, добавьте товар в корзину')
            return redirect('/')

    def post(self, *args, **kwargs):
        """Проверка на существование купона и применение его к заказу"""
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            coupon_code = form.cleaned_data.get('code')
            coupon = Coupon.objects.filter(code=coupon_code, status=True)
            if coupon.exists():
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = Coupon.objects.get(code=coupon_code)
                order.save()
                messages.info(self.request, f'Промокод {coupon_code} применен')
            else:
                messages.info(self.request, f'Промокода {coupon_code} не существует')
            return redirect('mainapp:cart')


class CheckoutView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, *args, **kwargs):
        if Order.objects.filter(user=self.request.user, ordered=False).exists():
            form = CheckoutForm()
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'form': form,
                'order': order
            }
            return render(self.request, 'mainapp/checkout.html', context)
        else:
            messages.info(self.request, 'Оформление невозможно, заказа не существует')
            return redirect('/')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        print(self.request.POST)
        if form.is_valid():
            order = Order.objects.get(user=self.request.user, ordered=False)
            order_type = form.cleaned_data.get('order_type')
            payment_type = form.cleaned_data.get('payment_type')
            delivery_name = form.cleaned_data.get('delivery_name')
            order.order_type = order_type
            order.payment_type = payment_type
            order.delivery_name = delivery_name

            order_products = order.products.all()
            order_products.update(ordered=True)
            for product in order_products:
                product.save()

            order.ordered_date = timezone.now()
            order.final_price = order.get_total_price()
            order.ordered = True
            order.save()

            messages.info(self.request, f'Заказ успешно оформлен')
            return redirect('/')


class OrdersFilterView(LoginRequiredMixin, FilterView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'mainapp/orders-history.html'
    context_object_name = 'orders'
    model = Order
    filterset_class = OrdersFilter

    def get_queryset(self):
        return self.model.objects.filter(ordered=True).order_by('-id')


class OrderDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Order
    context_object_name = 'order'
    template_name = 'mainapp/order_detail.html'


@login_required(login_url='/login/')
def add_to_cart_from_product_list(request, slug):
    return add_to_cart(request, slug, 'category')


@login_required(login_url='/login/')
def remove_single_product_from_product_list(request, slug):
    return remove_single_product(request, slug, 'category')


@login_required(login_url='/login/')
def add_to_cart_from_cart(request, slug):
    return add_to_cart(request, slug, 'cart', is_cart=True)


@login_required(login_url='/login/')
def remove_single_product_from_cart(request, slug):
    return remove_single_product(request, slug, 'cart', is_cart=True)


@login_required(login_url='/login/')
def remove_product_from_cart(request, slug):
    return remove_product(request, slug, 'cart', is_cart=True)
