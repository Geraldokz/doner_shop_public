from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone

from .models import Category, Product, OrderProduct, Order


def add_to_cart(request, slug, page_name, is_cart=False):
    product = get_object_or_404(Product, slug=slug)
    category = get_object_or_404(Category, name=product.category)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            if is_cart:
                return redirect(f'mainapp:{page_name}')
            else:
                messages.info(request, f'{product.name} - {order_product.quantity}')
                return redirect(f'mainapp:{page_name}', slug=category.slug)
        else:
            messages.info(request, f'{product.name} в корзине')
            order.products.add(order_product)
            if is_cart:
                return redirect(f'mainapp:{page_name}')
            else:
                return redirect(f'mainapp:{page_name}', slug=category.slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, f'{product.name} в корзине')
        if is_cart:
            return redirect(f'mainapp:{page_name}')
        else:
            return redirect(f'mainapp:{page_name}', slug=category.slug)


def remove_single_product(request, slug, page_name, is_cart=False):
    product = get_object_or_404(Product, slug=slug)
    category = get_object_or_404(Category, name=product.category)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
                order_product.delete()
            if is_cart:
                return redirect(f'mainapp:{page_name}')
            else:
                messages.info(request, f'{product.name} - {order_product.quantity}')
                return redirect(f'mainapp:{page_name}', slug=category.slug)
        else:
            messages.info(request, 'Товара нет в корзине')
            return redirect(f'mainapp:{page_name}', slug=category.slug)
    else:
        messages.info(request, 'Заказа не существует')
        return redirect(f'mainapp:{page_name}', slug=category.slug)


def remove_product(request, slug, page_name, is_cart=True):
    product = get_object_or_404(Product, slug=slug)
    category = get_object_or_404(Category, name=product.category)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            order_product.delete()
            if is_cart:
                return redirect(f'mainapp:{page_name}')
            else:
                messages.info(request, 'Товар удален из корзины')
                return redirect(f'mainapp:{page_name}', slug=category.slug)
        else:
            messages.info(request, 'Товара не было в корзине')
            return redirect('mainapp:category', slug=category.slug)
    else:
        messages.info(request, 'Заказа не существует')
        return redirect('mainapp:category', slug=category.slug)
