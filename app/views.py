from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login


#Crea algo para ver


"""
#Definimos una funcion
#Request es un parametro de django para darle un mensaje a la api
def helloworld(request):
    #dentro del string se puede escribir un codigo html
    return HttpResponse("Hola a todos")
"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Para guardar el usuario en una cookie
from django.contrib.auth import login, logout, authenticate
from .models import Task

#Segunda forma escalable
def helloworld(request):
    
    if request.method == 'GET':
        return render(request, 'pagina1.html', {
        'form': UserCreationForm
        })
        
    else:
        if request.POST["password1"] == request.POST["password2"]:
            #para registrar un usuario
            #Este user pide usuario y contraseña
            
            
            if User.objects.filter(username=request.POST["username"]).exists():
                user = authenticate(request, username=request.POST["username"], password=request.POST["password1"])
                if user is not None:
                    # Loguear al usuario si las credenciales son correctas
                    login(request, user)
                    return render(request, 'pagina1.html', {
                        'form': UserCreationForm(),
                        'error': 'Inicio de sesión exitoso.'
                    })
                else:
                    # Si la contraseña es incorrecta
                    return render(request, 'pagina1.html', {
                        'form': UserCreationForm(),
                        'error': 'Usuario ya existe, pero la contraseña es incorrecta.'
                    })
                """
                return render(request, 'pagina1.html', {
                    'form': UserCreationForm(),
                    'error': 'El nombre de usuario ya está en uso.'
                })
                """
            else:
                # Crear el usuario
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"]
                    ) 
                user.save()
                login(request, user)
                return render(request, 'pagina1.html', {
                    'form': UserCreationForm(),
                    'error': 'Usuario creado exitosamente.'
                    }) 
            
            """
            try:
                user = User.objects.create_user(username=request.POST["username"],
                                     password=request.POST["password1"])
                user.save()
                login(request, user)            
                return render(request, 'pagina1.html', {
                       'form': UserCreationForm,
                       'error': 'Usuario creado'
                       })              
            except: #IntegrityError: 
                return render(request, 'pagina1.html', {
                       'form': UserCreationForm,
                       'error': 'Usuario ya existe'
                       })
            """ 
        else:
            return render(request, 'pagina1.html', {
                       'form': UserCreationForm,
                       'error': 'Password no coincide'
                       })

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm()
        })
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(home)  # Redirige a la página de inicio o donde desees
        else:
            return render(request, 'login.html', {
                'form': form,
                'error': 'Usuario o contraseña incorrectos'
            })

@login_required       
def task(request):
    tasks = Task.objects.all()
    
    return render(request, "task.html", {
        "tasks":tasks
    })

def home(request):
    return render(request, "home.html")

def logout1(request):
    logout(request)
    return redirect(home)

from .forms import TaskForm

@login_required
def create_task(request):
    
    if request.method== "GET":
        return render(request, "create_task.html", {
            "form": TaskForm
            })
    else:
        try:
            form = TaskForm(request.POST)
            if form.is_valid():
                 new_task = form.save(commit=False)
                 new_task.user = request.user
                 new_task.save()
                 print(new_task)
                 return render(request, "create_task.html", {
                    "form": TaskForm,
                    "success": "Se creo correctamente"
                    })
            else:
                 print(form.errors)
                 raise ValueError("Invalidad data")
        except ValueError:
            return render(request, "create_task.html", {
                "form": TaskForm,
                "error": "Please provide valida data"
            })

@login_required
def task_detail(request, task_id):
    if request.method == "GET":
      task = get_object_or_404(Task, id=task_id)
      form = TaskForm(instance=task)
      return render(request, "task_details.html", {
          "task":task,
          "form":form
      })
    else:
        try:
            task = get_object_or_404(Task, id=task_id)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect(home) 
        except:
            return render(request, "task_details.html", {
                "task": task,
                "form": form,
                "error": "Error de update"
            })    
            
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect(home)
    
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect(home)
    
def tasks_completed(request):
    tasks = Task.objects-filter(user=request.user, datecompleted_isnull=False)
    
    return render(request, "task.html", {
        "tasks":tasks
    })