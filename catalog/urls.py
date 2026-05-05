from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/remove-all/<int:pk>/', views.remove_from_cart_all, name='remove_from_cart_all'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('cabinet/edit/', views.cabinet_edit, name='cabinet_edit'),
]