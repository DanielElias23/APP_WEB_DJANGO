from django.forms import ModelForm
from .models import Task, orders, brands, categories, customers, order_items, products, staffs, stocks, stores

#Creamos un formulario en base a una tabla ya creada
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "important"]
        
from django import forms


class OrderForm(forms.ModelForm):
    class Meta:
        model = orders
        fields = ["order_id",'customer_id', 'order_status', 'order_date', "required_date", "shipped_date", "store_id", "staff_id"]
        
class BrandForm(forms.ModelForm):
    class Meta:
        model = brands
        fields = ["brand_id",'brand_name']
        
class CategoriesForm(forms.ModelForm):
    class Meta:
        model = categories
        fields = ["category_id",'category_name']
        
class CustomersForm(forms.ModelForm):
    class Meta:
        model = customers
        fields = ["customer_id",'first_name', 'last_name', 'phone', "email", "street", "city", "state", "zip_code"]
        
class Order_ItemsForm(forms.ModelForm):
    class Meta:
        model = order_items
        fields = ["order_id",'item_id', 'product_id', 'quantity', "list_price", "discount"]
        
class ProductsForm(forms.ModelForm):
    class Meta:
        model = products
        fields = ["product_id", 'brand_id', 'category_id', "model_year", "list_price", 'product_name']
        
class StaffsForm(forms.ModelForm):
    class Meta:
        model = staffs
        fields = ["staff_id", 'first_name', 'last_name', "email", "phone", 'active', 'manager_id', 'store_id']
        
class StocksForm(forms.ModelForm):
    class Meta:
        model = stocks
        fields = ["store_id", 'product_id', 'quantity']
        
class StoresForm(forms.ModelForm):
    class Meta:
        model = stores
        fields = ["store_id", 'store_name', 'phone', "email", "street", 'city', 'state', 'zip_code']