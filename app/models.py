from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
 
    def __str__(self):
        return self.title + "- by " + self.user.username
 

class brands(models.Model):
    brand_id = models.IntegerField(unique=True)
    brand_name = models.CharField(max_length=100, null=True, blank=True)
 
class categories(models.Model):
    category_id = models.IntegerField()
    category_name = models.CharField(max_length=100, null=True, blank=True)
    
class customers(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    
class order_items(models.Model):
    order_id = models.IntegerField()
    item_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField(null=True, blank=True)
    list_price = models.FloatField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    
class orders(models.Model):
    order_id = models.IntegerField()
    customer_id = models.IntegerField()
    order_status = models.IntegerField(null=True, blank=True)
    order_date = models.CharField(max_length=100, null=True, blank=True)
    required_date = models.CharField(max_length=100, null=True, blank=True)
    shipped_date = models.CharField(max_length=100, null=True, blank=True)
    store_id = models.IntegerField(null=True, blank=True)
    staff_id = models.IntegerField(null=True, blank=True)
    
class products(models.Model):
    product_id = models.IntegerField()
    brand_id = models.IntegerField()
    category_id = models.IntegerField()
    model_year = models.IntegerField(null=True, blank=True)
    list_price = models.FloatField(null=True, blank=True)
    product_name = models.CharField(max_length=100, null=True, blank=True)
    
class staffs(models.Model):
    staff_id = models.IntegerField()
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    active = models.IntegerField()                        
    manager_id = models.IntegerField(null=True, blank=True)
    store_id = models.IntegerField(null=True, blank=True)

class stocks(models.Model):
    store_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField(null=True, blank=True)
    
class stores(models.Model):
    store_id = models.IntegerField()
    store_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=100, null=True, blank=True)
    
#Hay que ejecutar para que django cree una tabla automaticamente con:   
#python3 manage.py makemigrations

#Luego para activarla:
#python manage.py migrate
