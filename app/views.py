from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .models import brands, categories, customers, order_items, orders, products, staffs, stocks, stores
from .forms import OrderForm, CategoriesForm, CustomersForm, BrandForm, Order_ItemsForm, ProductsForm, StaffsForm, StocksForm, StoresForm
from django.db.models import Count
from django.contrib import messages
from django.db.models import Max
import csv
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
        return render(request, 'suscribe.html', {
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
                    return render(request, 'suscribe.html', {
                        'form': UserCreationForm(),
                        'success': 'Inicio de sesión exitoso.'
                    })
                else:
                    # Si la contraseña es incorrecta
                    return render(request, 'suscribe.html', {
                        'form': UserCreationForm(),
                        'error': 'Usuario ya existe, pero la contraseña es incorrecta.'
                    })

            else:
                # Crear el usuario
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"]
                    ) 
                user.save()
                #login(request, user)
                return render(request, 'suscribe.html', {
                    'form': UserCreationForm(),
                    'success': 'Felicitaciones el usuario ha sido creado exitosamente'
                    }) 
            
        else:
            return render(request, 'suscribe.html', {
                       'form': UserCreationForm,
                       'error': 'La contraseña no coincide'
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
    
    
####################################################################################33    

def brands_list(request):
    # Eliminación: Si se recibe 'delete' en la URL, se elimina la marca.
    if 'delete' in request.GET:
        brand_to_delete = get_object_or_404(brands, brand_id=request.GET['delete'])
        brand_to_delete.delete()
        return redirect('brands_list')

    Brands = brands.objects.all()
    
    brand_id   = request.GET.get('brand_id')
    brand_name = request.GET.get('brand_name')
    
    if brand_id:
        Brands = Brands.filter(brand_id=brand_id)
        if not Brands.exists():
            messages.warning(request, f"No se encontró ninguna marca con ID {brand_id}.")
    if brand_name:
        Brands = Brands.filter(brand_name=brand_name)
    
    if request.method == 'POST':
        # Si se envía 'brand_id', se está actualizando una marca existente
        if 'brand_id' in request.POST:
            brand_instance = get_object_or_404(brands, brand_id=request.POST['brand_id'])
            form = BrandForm(request.POST, instance=brand_instance)
        else:
            form = BrandForm(request.POST)
        
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('brands_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        if brand_id:
            brand = brands.objects.filter(brand_id=brand_id).first()
            if brand:
                form = BrandForm(instance=brand)
            else:
                form = BrandForm()
        else:
            form = BrandForm()

    return render(request, 'brands_list.html', {
        'Brands': Brands,
        'form': form
    })

def create_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            new_brand = form.save(commit=False)
            # Si el usuario ingresa manualmente un ID, lo usamos; de lo contrario, se genera automáticamente.
            if request.POST.get('brand_id'):
                new_brand.brand_id = request.POST['brand_id']
            else:
                max_brand_id = brands.objects.aggregate(Max('brand_id'))['brand_id__max']
                new_brand.brand_id = (max_brand_id + 1) if max_brand_id else 1
            new_brand.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'new_brand_id': new_brand.brand_id,
                    'brand_name': new_brand.brand_name
                })
            messages.success(request, 'Marca creada exitosamente.')
            return redirect('brands_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            messages.error(request, 'Hubo un error al crear la marca. Verifica los datos ingresados.')
    else:
        form = BrandForm()
    return render(request, 'brands_list.html', {'form': form})

def download_brands(request):
    brands_qs = brands.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="brands.csv"'
    writer = csv.writer(response)
    writer.writerow(['Brand_ID', 'Brand_Name'])
    for brand in brands_qs:
        writer.writerow([
            brand.brand_id,
            brand.brand_name
        ])
    return response
    

###########################################################################################################


def categories_list(request):
    # Eliminación de categoría (vía GET)
    if 'delete' in request.GET:
        category_to_delete = get_object_or_404(categories, category_id=request.GET['delete'])
        category_to_delete.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Categoría eliminada'})
        return redirect('categories_list')
    
    Categories = categories.objects.all()
    
    category_id = request.GET.get('category_id')
    category_name = request.GET.get('category_name')
    
    if category_id:
        Categories = Categories.filter(category_id=category_id)
        if not Categories.exists():
            messages.warning(request, f"No se encontró ninguna categoría con ID {category_id}.")
    if category_name:
        Categories = Categories.filter(category_name=category_name)
    
    if request.method == 'POST':
        # Si se envía 'category_id', se actualiza una categoría existente
        if 'category_id' in request.POST:
            category_instance = get_object_or_404(categories, category_id=request.POST['category_id'])
            form = CategoriesForm(request.POST, instance=category_instance)
        else:
            form = CategoriesForm(request.POST)
        
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('categories_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        # Opcional: si se filtra por ID se puede cargar el formulario con la categoría encontrada
        if category_id:
            category_obj = categories.objects.filter(category_id=category_id).first()
            if category_obj:
                form = CategoriesForm(instance=category_obj)
            else:
                form = CategoriesForm()
        else:
            form = CategoriesForm()
    
    return render(request, 'categories_list.html', {
        'Categories': Categories,
        'form': form
    })


def create_categories(request):
    if request.method == 'POST':
        form = CategoriesForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            max_category_id = categories.objects.aggregate(Max('category_id'))['category_id__max']
            new_category.category_id = (max_category_id + 1) if max_category_id else 1
            new_category.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'new_category_id': new_category.category_id,
                    'category_name': new_category.category_name
                })
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('categories_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            messages.error(request, 'Hubo un error al crear la categoría. Verifica los datos ingresados.')
    else:
        form = CategoriesForm()
    return render(request, 'categories_list.html', {'form': form})


def download_categories(request):
    categories_qs = categories.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="categories.csv"'
    writer = csv.writer(response)
    writer.writerow(['Category_ID', 'Category_Name'])
    for category in categories_qs:
        writer.writerow([
            category.category_id,
            category.category_name
        ])
    return response

###########################################################################################################

def customers_list(request):
    # Eliminación: se utiliza la clave primaria (pk) para identificar el registro de forma única.
    if 'delete' in request.GET:
        customer_to_delete = get_object_or_404(customers, pk=request.GET['delete'])
        customer_to_delete.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Cliente eliminado'})
        return redirect('customers_list')
    
    Customers = customers.objects.all()
    state_statuses = customers.objects.values_list('state', flat=True).distinct()
    
    customer_id = request.GET.get('customer_id')
    first_name  = request.GET.get('first_name')
    last_name   = request.GET.get('last_name')
    phone       = request.GET.get('phone')
    email       = request.GET.get('email')
    street      = request.GET.get('street')
    city        = request.GET.get('city')
    state       = request.GET.get('state')
    zip_code    = request.GET.get('zip_code')
    
    if customer_id:
        Customers = Customers.filter(customer_id=customer_id)
    if first_name:
        Customers = Customers.filter(first_name=first_name)
    if last_name:
        Customers = Customers.filter(last_name=last_name)
    if phone:
        Customers = Customers.filter(phone=phone)
    if email:
        Customers = Customers.filter(email=email)
    if street:
        Customers = Customers.filter(street=street)
    if city:
        Customers = Customers.filter(city=city)
    if state:
        Customers = Customers.filter(state=state)
    if zip_code:
        Customers = Customers.filter(zip_code=zip_code)
    
    if request.method == 'POST':
        # Para actualización, se espera que la petición POST incluya el campo 'id' (la pk)
        if 'id' in request.POST:
            customer_instance = get_object_or_404(customers, pk=request.POST['id'])
            form = CustomersForm(request.POST, instance=customer_instance)
        else:
            form = CustomersForm(request.POST)
        
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('customers_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        # Si se filtra por customer_id, se carga el formulario con un registro (cualquiera) que cumpla con ese valor
        if customer_id:
            customer_obj = customers.objects.filter(customer_id=customer_id).first()
            form = CustomersForm(instance=customer_obj) if customer_obj else CustomersForm()
        else:
            form = CustomersForm()
    
    customer_status_counts = Customers.values('state').annotate(count=Count('state'))
    
    return render(request, 'customers_list.html', {
        'Customers': Customers,
        'form': form,
        'state_statuses': state_statuses,
        'order_status_counts': customer_status_counts
    })

def create_customer(request):
    if request.method == 'POST':
        form = CustomersForm(request.POST)
        if form.is_valid():
            # Se guarda utilizando los datos ingresados por el usuario; el valor de customer_id se ingresa manualmente.
            new_customer = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'new_customer_id': new_customer.customer_id,
                    'first_name': new_customer.first_name,
                    'last_name': new_customer.last_name,
                    'phone': new_customer.phone,
                    'email': new_customer.email,
                    'street': new_customer.street,
                    'city': new_customer.city,
                    'state': new_customer.state,
                    'zip_code': new_customer.zip_code,
                    'pk': new_customer.pk
                })
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('customers_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            messages.error(request, 'Hubo un error al crear el cliente. Verifica los datos ingresados.')
    else:
        form = CustomersForm()
    return render(request, 'customers_list.html', {'form': form})

def download_customers(request):
    orders_qs = customers.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'
    writer = csv.writer(response)
    writer.writerow(['Customer ID', 'First Name', 'Last Name', 'Phone', 'Email', 'Street', 'City', 'State', 'Zip code'])
    for customer in orders_qs:
        writer.writerow([
            customer.customer_id,
            customer.first_name,
            customer.last_name,
            customer.phone,
            customer.email,
            customer.street,
            customer.city,
            customer.state,
            customer.zip_code
        ])
    return response

###########################################################################################################
    
def order_items_list(request):
    # Eliminación: si se recibe el parámetro 'delete' en GET, se elimina el ítem de orden.
    if 'delete' in request.GET:
        order_to_delete = get_object_or_404(order_items, order_id=request.GET['delete'])
        order_to_delete.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Ítem de orden eliminado'})
        return redirect('order_items_list')
    
    Order_items = order_items.objects.all()
    
    # Filtrado según parámetros GET
    order_id    = request.GET.get('order_id')
    item_id     = request.GET.get('item_id')
    product_id  = request.GET.get('product_id')
    quantity    = request.GET.get('quantity')
    list_price  = request.GET.get('list_price')
    discount    = request.GET.get('discount')
    
    if order_id:
        Order_items = Order_items.filter(order_id=order_id)
        if not Order_items.exists():
            messages.warning(request, f"No se encontró ninguna orden con ID {order_id}.")
    if item_id:
        Order_items = Order_items.filter(item_id=item_id)
    if product_id:
        Order_items = Order_items.filter(product_id=product_id)
    if quantity:
        Order_items = Order_items.filter(quantity=quantity)
    if list_price:
        Order_items = Order_items.filter(list_price=list_price)
    if discount:
        Order_items = Order_items.filter(discount=discount)
    
    # Procesar actualización mediante POST
    if request.method == 'POST':
        if 'order_id' in request.POST:
            order_instance = get_object_or_404(order_items, order_id=request.POST['order_id'])
            form = Order_ItemsForm(request.POST, instance=order_instance)
        else:
            form = Order_ItemsForm(request.POST)
        
        if form.is_valid():
            form.save()  # Se utiliza el valor ingresado por el usuario para order_id
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('order_items_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        if order_id:
            order_obj = order_items.objects.filter(order_id=order_id).first()
            form = Order_ItemsForm(instance=order_obj) if order_obj else Order_ItemsForm()
        else:
            form = Order_ItemsForm()
    
    order_status_counts = Order_items.values('quantity').annotate(count=Count('quantity'))
    
    return render(request, 'order_items_list.html', {
        'Order_items': Order_items,
        'form': form,
        'order_status_counts': order_status_counts
    })

def create_order_items(request):
    if request.method == 'POST':
        form = Order_ItemsForm(request.POST)
        if form.is_valid():
            # Se guarda directamente usando el valor ingresado, sin asignar automáticamente el ID.
            new_order = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'new_order_id': new_order.order_id,
                    'item_id': new_order.item_id,
                    'product_id': new_order.product_id,
                    'quantity': new_order.quantity,
                    'list_price': new_order.list_price,
                    'discount': new_order.discount,
                })
            messages.success(request, 'Orden creada exitosamente.')
            return redirect('order_items_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            messages.error(request, 'Hubo un error al crear la orden. Verifica los datos ingresados.')
    else:
        form = Order_ItemsForm()
    return render(request, 'order_items_list.html', {'form': form})

def download_order_items(request):
    orders_qs = order_items.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_items.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Item ID', 'Product ID', 'Quantity', 'List Price', 'Discount'])
    for order_item in orders_qs:
        writer.writerow([
            order_item.order_id,
            order_item.item_id,
            order_item.product_id,
            order_item.quantity,
            order_item.list_price,
            order_item.discount,
        ])
    return response

#######################################################################################################################

def orders_list(request):
    # Eliminación: si se recibe el parámetro 'delete' en GET, se elimina la orden.
    if 'delete' in request.GET:
        order_to_delete = get_object_or_404(orders, order_id=request.GET['delete'])
        order_to_delete.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Orden eliminada'})
        return redirect('orders_list')
    
    Orders = orders.objects.all()
    order_statuses = orders.objects.values_list('order_status', flat=True).distinct()
    
    order_id     = request.GET.get('order_id')
    customer_id  = request.GET.get('customer_id')
    order_status = request.GET.get('order_status')
    start_date   = request.GET.get('start_date')
    end_date     = request.GET.get('end_date')
    required_date= request.GET.get('required_date')
    shipped_date = request.GET.get('shipped_date')
    store_id     = request.GET.get('store_id')
    staff_id     = request.GET.get('staff_id')
    
    if order_id:
        Orders = Orders.filter(order_id=order_id)
        if not Orders.exists():
            messages.warning(request, f"No se encontró ninguna orden con ID {order_id}.")
    if customer_id:
        Orders = Orders.filter(customer_id=customer_id)
    if order_status:
        Orders = Orders.filter(order_status__icontains=order_status)
    if start_date and end_date:
        Orders = Orders.filter(order_date__range=[start_date, end_date])
    if required_date:
        Orders = Orders.filter(required_date=required_date)
    if shipped_date:
        Orders = Orders.filter(shipped_date=shipped_date)
    if store_id:
        Orders = Orders.filter(store_id=store_id)
    if staff_id:
        Orders = Orders.filter(staff_id=staff_id)
    
    if request.method == 'POST':
        if 'order_id' in request.POST:
            order_instance = get_object_or_404(orders, order_id=request.POST['order_id'])
            form = OrderForm(request.POST, instance=order_instance)
        else:
            form = OrderForm(request.POST)
        
        if form.is_valid():
            form.save()  # Se utiliza el valor ingresado por el usuario para order_id.
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('orders_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        if order_id:
            order_obj = orders.objects.filter(order_id=order_id).first()
            form = OrderForm(instance=order_obj) if order_obj else OrderForm()
        else:
            form = OrderForm()
    
    order_status_counts = Orders.values('order_status').annotate(count=Count('order_status'))
    
    return render(request, 'orders_list.html', {
        'Orders': Orders,
        'form': form,
        'order_statuses': order_statuses,
        'order_status_counts': order_status_counts
    })

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Se guarda utilizando el valor ingresado por el usuario; no se autoasigna el order_id.
            new_order = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'new_order_id': new_order.order_id,
                    'customer_id': new_order.customer_id,
                    'order_status': new_order.order_status,
                    'order_date': new_order.order_date,
                    'required_date': new_order.required_date,
                    'shipped_date': new_order.shipped_date,
                    'store_id': new_order.store_id,
                    'staff_id': new_order.staff_id,
                })
            messages.success(request, 'Orden creada exitosamente.')
            return redirect('orders_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            messages.error(request, 'Hubo un error al crear la orden. Verifica los datos ingresados.')
    else:
        form = OrderForm()
    return render(request, 'orders_list.html', {'form': form})

def download_orders(request):
    orders_qs = orders.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer ID', 'Order Status', 'Order Date', 'Required Date', 'Shipped Date', 'Store ID', 'Staff ID'])
    for order in orders_qs:
        writer.writerow([
            order.order_id,
            order.customer_id,
            order.order_status,
            order.order_date,
            order.required_date,
            order.shipped_date,
            order.store_id,
            order.staff_id
        ])
    return response

##########################################################################################################

def products_list(request):
    # Eliminación: si se recibe el parámetro 'delete' en GET, se elimina el producto.
    if 'delete' in request.GET:
        product_to_delete = get_object_or_404(products, product_id=request.GET['delete'])
        product_to_delete.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Producto eliminado'})
        return redirect('products_list')
    
    Products = products.objects.all()
    
    product_id   = request.GET.get('product_id')
    product_name = request.GET.get('product_name')
    brand_id     = request.GET.get('brand_id')
    category_id  = request.GET.get('category_id')
    model_year   = request.GET.get('model_year')
    list_price   = request.GET.get('list_price')
    
    if product_id:
        Products = Products.filter(product_id=product_id)
        if not Products.exists():
            messages.warning(request, f"No se encontró ningún producto con ID {product_id}.")
    if product_name:
        Products = Products.filter(product_name=product_name)
    if brand_id:
        Products = Products.filter(brand_id=brand_id)
    if category_id:
        Products = Products.filter(category_id=category_id)
    if model_year:
        Products = Products.filter(model_year=model_year)
    if list_price:
        Products = Products.filter(list_price=list_price)
    
    if request.method == 'POST':
        # Si se envía product_id en POST se actualiza el producto existente.
        if 'product_id' in request.POST:
            product_instance = get_object_or_404(products, product_id=request.POST['product_id'])
            form = ProductsForm(request.POST, instance=product_instance)
        else:
            form = ProductsForm(request.POST)
        
        if form.is_valid():
            form.save()  # Se utiliza el valor ingresado por el usuario para product_id.
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('products_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        if product_id:
            product_obj = products.objects.filter(product_id=product_id).first()
            form = ProductsForm(instance=product_obj) if product_obj else ProductsForm()
        else:
            form = ProductsForm()
    
    # Ejemplo de agrupación para el gráfico: número de productos agrupados por lista de precio.
    product_price_counts = Products.values('list_price').annotate(count=Count('list_price'))
    
    return render(request, 'products_list.html', {
        'Products': Products,
        'form': form,
        'order_status_counts': product_price_counts,  # Se usa para el gráfico.
    })

def create_products(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST)
        if form.is_valid():
            # Se guarda utilizando el valor ingresado por el usuario.
            new_product = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'new_product_id': new_product.product_id,
                    'brand_id': new_product.brand_id,
                    'category_id': new_product.category_id,
                    'model_year': new_product.model_year,
                    'list_price': new_product.list_price,
                    'product_name': new_product.product_name,
                })
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('products_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            messages.error(request, 'Hubo un error al crear el producto. Verifica los datos ingresados.')
    else:
        form = ProductsForm()
    return render(request, 'products_list.html', {'form': form})

def download_products(request):
    products_qs = products.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    writer = csv.writer(response)
    writer.writerow(['Product ID', 'Product Name', 'Brand ID', 'Category ID', 'Model Year', 'List Price'])
    for product in products_qs:
        writer.writerow([
            product.product_id,
            product.product_name,
            product.brand_id,
            product.category_id,
            product.model_year,
            product.list_price,
        ])
    return response

##########################################################################################################

def staffs_list(request):
    # Eliminación: si se recibe 'delete' en GET, se elimina el empleado.
    if 'delete' in request.GET:
        staff_to_delete = get_object_or_404(staffs, staff_id=request.GET['delete'])
        staff_to_delete.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Empleado eliminado'})
        return redirect('staffs_list')
    
    Staffs = staffs.objects.all()
    
    staff_id   = request.GET.get('staff_id')
    first_name = request.GET.get('first_name')
    last_name  = request.GET.get('last_name')
    email      = request.GET.get('email')
    phone      = request.GET.get('phone')
    active     = request.GET.get('active')
    store_id   = request.GET.get('store_id')
    manager_id = request.GET.get('manager_id')
    
    if staff_id:
        Staffs = Staffs.filter(staff_id=staff_id)
        if not Staffs.exists():
            messages.warning(request, f"No se encontró ningún empleado con ID {staff_id}.")
    if first_name:
        Staffs = Staffs.filter(first_name=first_name)
    if last_name:
        Staffs = Staffs.filter(last_name=last_name)
    if email:
        Staffs = Staffs.filter(email=email)
    if phone:
        Staffs = Staffs.filter(phone=phone)
    if active:
        Staffs = Staffs.filter(active=active)
    if store_id:
        Staffs = Staffs.filter(store_id=store_id)
    if manager_id:
        Staffs = Staffs.filter(manager_id=manager_id)
    
    if request.method == 'POST':
        # Si se envía staff_id en POST, se actualiza el registro existente.
        if 'staff_id' in request.POST:
            staff_instance = get_object_or_404(staffs, staff_id=request.POST['staff_id'])
            form = StaffsForm(request.POST, instance=staff_instance)
        else:
            form = StaffsForm(request.POST)
        
        if form.is_valid():
            form.save()  # Se guarda usando el valor ingresado por el usuario.
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('staffs_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        if staff_id:
            staff_obj = staffs.objects.filter(staff_id=staff_id).first()
            form = StaffsForm(instance=staff_obj) if staff_obj else StaffsForm()
        else:
            form = StaffsForm()
    
    # Agrupación para el gráfico (por ejemplo, cantidad de empleados según el valor de 'active')
    staff_status_counts = Staffs.values('active').annotate(count=Count('active'))
    
    return render(request, 'staffs_list.html', {
        'Staffs': Staffs,
        'form': form,
        'order_status_counts': staff_status_counts
    })

def create_staffs(request):
    if request.method == 'POST':
        form = StaffsForm(request.POST)
        if form.is_valid():
            # Se guarda directamente utilizando el valor ingresado por el usuario (sin autoasignación)
            new_staff = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'new_staff_id': new_staff.staff_id,
                    'first_name': new_staff.first_name,
                    'last_name': new_staff.last_name,
                    'email': new_staff.email,
                    'phone': new_staff.phone,
                    'active': new_staff.active,
                    'store_id': new_staff.store_id,
                    'manager_id': new_staff.manager_id,
                })
            messages.success(request, 'Empleado creado exitosamente.')
            return redirect('staffs_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            messages.error(request, 'Hubo un error al crear el empleado. Verifica los datos ingresados.')
    else:
        form = StaffsForm()
    return render(request, 'staffs_list.html', {'form': form})

def download_staffs(request):
    staffs_qs = staffs.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="staffs.csv"'
    writer = csv.writer(response)
    writer.writerow(['Staff ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Active', 'Store ID', 'Manager ID'])
    for staff in staffs_qs:
        writer.writerow([
            staff.staff_id,
            staff.first_name,
            staff.last_name,
            staff.email,
            staff.phone,
            staff.active,
            staff.store_id,
            staff.manager_id,
        ])
    return response

#########################################################################################################

def stocks_list(request):
    # Eliminación: se utiliza la clave primaria (pk) para identificar el registro.
    if 'delete' in request.GET:
        stock_to_delete = get_object_or_404(stocks, pk=request.GET['delete'])
        stock_to_delete.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Stock eliminado'})
        return redirect('stocks_list')
    
    Stocks = stocks.objects.all()
    
    store_id   = request.GET.get('store_id')
    product_id = request.GET.get('product_id')
    quantity   = request.GET.get('quantity')
    
    if store_id:
        Stocks = Stocks.filter(store_id=store_id)
        if not Stocks.exists():
            messages.warning(request, f"No se encontró ningún registro con la tienda ID {store_id}.")
    if product_id:
        Stocks = Stocks.filter(product_id=product_id)
    if quantity:
        Stocks = Stocks.filter(quantity=quantity)
    
    if request.method == 'POST':
        # Para actualización se espera recibir el campo "id" (la pk)
        if 'id' in request.POST:
            stock_instance = get_object_or_404(stocks, pk=request.POST['id'])
            form = StocksForm(request.POST, instance=stock_instance)
        else:
            form = StocksForm(request.POST)
        
        if form.is_valid():
            form.save()  # Se guardan los datos ingresados, sin modificar store_id
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('stocks_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        if store_id:
            stock_obj = stocks.objects.filter(store_id=store_id).first()
            form = StocksForm(instance=stock_obj) if stock_obj else StocksForm()
        else:
            form = StocksForm()
    
    # Agrupar para el gráfico: por ejemplo, cantidad de registros agrupados por "quantity"
    stock_quantity_counts = Stocks.values('quantity').annotate(count=Count('quantity'))
    
    return render(request, 'stocks_list.html', {
        'Stocks': Stocks,
        'form': form,
        'order_status_counts': stock_quantity_counts
    })

def create_stocks(request):
    if request.method == 'POST':
        form = StocksForm(request.POST)
        if form.is_valid():
            # Se guarda utilizando los datos ingresados manualmente
            new_stock = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'new_store_id': new_stock.store_id,
                    'product_id': new_stock.product_id,
                    'quantity': new_stock.quantity,
                    'pk': new_stock.pk  # clave primaria para identificar el registro
                })
            messages.success(request, 'Stock creado exitosamente.')
            return redirect('stocks_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            messages.error(request, 'Hubo un error al crear el stock. Verifica los datos ingresados.')
    else:
        form = StocksForm()
    return render(request, 'stocks_list.html', {'form': form})

def download_stocks(request):
    stocks_qs = stocks.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stocks.csv"'
    writer = csv.writer(response)
    writer.writerow(['Store ID', 'Product ID', 'Quantity'])
    for stock in stocks_qs:
        writer.writerow([
            stock.store_id,
            stock.product_id,
            stock.quantity,
        ])
    return response



#########################################################################################################

def stores_list(request):
    # Eliminación: se usa la clave primaria (pk) para identificar de forma única el registro,
    # de modo que se pueda eliminar aunque store_id se repita.
    if 'delete' in request.GET:
        store_to_delete = get_object_or_404(stores, pk=request.GET['delete'])
        store_to_delete.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Tienda eliminada'})
        return redirect('stores_list')
    
    Stores = stores.objects.all()
    
    # Filtros de búsqueda (filtrando por los valores ingresados por el usuario)
    store_id   = request.GET.get('store_id')
    store_name = request.GET.get('store_name')
    phone      = request.GET.get('phone')
    email      = request.GET.get('email')
    street     = request.GET.get('street')
    city       = request.GET.get('city')
    state      = request.GET.get('state')
    zip_code   = request.GET.get('zip_code')
    
    if store_id:
        Stores = Stores.filter(store_id=store_id)
        if not Stores.exists():
            messages.warning(request, f"No se encontró ninguna tienda con ID {store_id}.")
    if store_name:
        Stores = Stores.filter(store_name=store_name)
    if phone:
        Stores = Stores.filter(phone=phone)
    if email:
        Stores = Stores.filter(email=email)
    if street:
        Stores = Stores.filter(street=street)
    if city:
        Stores = Stores.filter(city=city)
    if state:
        Stores = Stores.filter(state=state)
    if zip_code:
        Stores = Stores.filter(zip_code=zip_code)
    
    if request.method == 'POST':
        # Para actualización, se espera recibir el parámetro 'id' (la clave primaria)
        if 'id' in request.POST:
            store_instance = get_object_or_404(stores, pk=request.POST['id'])
            form = StoresForm(request.POST, instance=store_instance)
        else:
            form = StoresForm(request.POST)
        
        if form.is_valid():
            form.save()  # Se guardan los datos ingresados manualmente
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('stores_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        # Se carga el formulario; si se filtra por store_id, se intenta cargar un registro (puede ser uno cualquiera)
        if store_id:
            store_obj = stores.objects.filter(store_id=store_id).first()
            form = StoresForm(instance=store_obj) if store_obj else StoresForm()
        else:
            form = StoresForm()
    
    # Para el gráfico, agrupamos por "state" (por ejemplo)
    store_state_counts = Stores.values('state').annotate(count=Count('state'))
    
    return render(request, 'stores_list.html', {
        'Stores': Stores,
        'form': form,
        'order_status_counts': store_state_counts
    })

def create_stores(request):
    if request.method == 'POST':
        form = StoresForm(request.POST)
        if form.is_valid():
            # Se guarda utilizando los datos ingresados manualmente (store_id se ingresa por el usuario)
            new_store = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Se devuelve también la clave primaria (pk) para identificar el registro de forma única
                return JsonResponse({
                    'status': 'success',
                    'new_store_id': new_store.store_id,
                    'store_name': new_store.store_name,
                    'phone': new_store.phone,
                    'email': new_store.email,
                    'street': new_store.street,
                    'city': new_store.city,
                    'state': new_store.state,
                    'zip_code': new_store.zip_code,
                    'pk': new_store.pk
                })
            messages.success(request, 'Tienda creada exitosamente.')
            return redirect('stores_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            messages.error(request, 'Hubo un error al crear la tienda. Verifica los datos ingresados.')
    else:
        form = StoresForm()
    return render(request, 'stores_list.html', {'form': form})

def download_stores(request):
    stores_qs = stores.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stores.csv"'
    writer = csv.writer(response)
    writer.writerow(['Store ID', 'Store Name', 'Phone', 'Email', 'Street', 'City', 'State', 'Zip Code'])
    for store in stores_qs:
        writer.writerow([
            store.store_id,
            store.store_name,
            store.phone,
            store.email,
            store.street,
            store.city,
            store.state,
            store.zip_code,
        ])
    return response

#########################################################################################################

def tables(request):
    return render(request, 'tables.html')