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
 
#Hay que ejecutar para que django cree una tabla automaticamente con:   
#python3 manage.py makemigrations

#Luego para activarla:
#python manage.py migrate
