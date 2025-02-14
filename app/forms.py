from django.forms import ModelForm
from .models import Task

#Creamos un formulario en base a una tabla ya creada
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "important"]