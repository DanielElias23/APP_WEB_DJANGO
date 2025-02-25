"""
URL configuration for api_datos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

#En esta seccion se ocupan otras funciones
from django.contrib import admin
from django.urls import path

#importacion de app de vista creadas
from app import views

#Son las rutas para que reconosca lo implementado
#Se ejecutan por orden las paginas
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path("home/task", views.task),
    path("home/create_task", views.create_task),
    path("home/<int:task_id>", views.task_detail, name="task_detail"),
    path("home/task_completed", views.tasks_completed),
    path("home/<int:task_id>/complete", views.complete_task, name="complete_task"),
    path("home/<int:task_id>/delete", views.delete_task, name="delete_task"),
    path('login/', views.login_view, name='login'),
    #app creada
    path('', views.helloworld),
    #para que el envio de formulario se haga,
    path('home/suscribe', views.helloworld, name="suscribe"),
    path('home/logout/', views.logout1),
    path('customers/', views.customers_list, name='customers_list'),
    path('brands/', views.brands_list, name='brands_list'),
    path('brands/create/', views.create_brand, name='create_brand'),
    path('download_brands/', views.download_brands, name='download_brands'),
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/create/', views.create_categories, name='create_categories'),
    path('download_categories/', views.download_categories, name='download_categories'),
    path('customers/', views.customers_list, name='customers_list'),
    path('customers/create/', views.create_customer, name='create_customer'),
    path('download_customers/', views.download_customers, name='download_customers'),
    path('order_items/', views.order_items_list, name='order_items_list'),
    path('order_items/create/', views.create_order_items, name='create_order_items'),
    path('download_order_items/', views.download_order_items, name='download_order_items'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/create/', views.create_order, name='create_order'),
    path('download_orders/', views.download_orders, name='download_orders'),
    path('products/', views.products_list, name='products_list'),
    path('products/create/', views.create_products, name='create_products'),
    path('download_products/', views.download_products, name='download_products'),
    path('staffs/', views.staffs_list, name='staffs_list'),
    path('staffs/create/', views.create_staffs, name='create_staffs'),
    path('download_staffs/', views.download_staffs, name='download_staffs'),
    path('stocks/', views.stocks_list, name='stocks_list'),
    path('stocks/create/', views.create_stocks, name='create_stocks'),
    path('download_stocks/', views.download_stocks, name='download_stocks'),
    path('stores/', views.stores_list, name='stores_list'),
    path('stores/create/', views.create_stores, name='create_stores'),
    path('download_stores/', views.download_stores, name='download_stores'),
    path('tables/', views.tables, name='tables'),
]
