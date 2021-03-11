from django.urls import path

from .views import (
    get_menu_page,
    CategoriesView,
    ProductsView,
    CartView,
    CheckoutView,
    OrdersFilterView,
    OrderDetailView,
    add_to_cart_from_product_list,
    add_to_cart_from_cart,
    remove_single_product_from_cart,
    remove_single_product_from_product_list,
    remove_product_from_cart
)

app_name = 'mainapp'

urlpatterns = [
    path('', CategoriesView.as_view(), name='main_page'),
    path('category/<slug>/', ProductsView.as_view(), name='category'),
    path('cart/', CartView.as_view(), name='cart'),
    path('menu/', get_menu_page, name='menu_page'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders-history/', OrdersFilterView.as_view(), name='orders-history'),
    path('orders-history/order-details/<pk>', OrderDetailView.as_view(), name='order-detail'),

    path('add-to-cart-from-product-list/<slug>/', add_to_cart_from_product_list, name='add-to-cart-from-product-list'),
    path('add-to-cart-from-cart/<slug>/', add_to_cart_from_cart, name='add-to-cart-from-cart'),
    path('remove-single-product-from-cart/<slug>/', remove_single_product_from_cart,
         name='remove-single-product-from-cart'),
    path('remove-single-product-from-product-list/<slug>/', remove_single_product_from_product_list,
         name='remove-single-product-from-product-list'),
    path('remove-product-from-cart/<slug>/', remove_product_from_cart, name='remove-product-from-cart'),
]
