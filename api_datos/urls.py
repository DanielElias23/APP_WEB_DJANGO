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
    path('home/pagina1', views.helloworld),
    path('home/logout/', views.logout1)
]
