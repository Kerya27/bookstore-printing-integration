"""
URL configuration for bookstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='catalog'), name='logout'),
    #admin panel
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/orders/', views.admin_orders, name='admin_orders'),
    path('admin-panel/orders/<int:pk>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-panel/orders/<int:pk>/status/', views.admin_order_status, name='admin_order_status'),
    path('admin-panel/books/', views.admin_books, name='admin_books'),
    path('admin-panel/books/add/', views.admin_book_add, name='admin_book_add'),
    path('admin-panel/books/<int:pk>/edit/', views.admin_book_edit, name='admin_book_edit'),
    path('admin-panel/books/<int:pk>/delete/', views.admin_book_delete, name='admin_book_delete'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('cart/add-ajax/<int:pk>/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('admin-panel/export/orders/', views.admin_export_orders, name='admin_export_orders'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
