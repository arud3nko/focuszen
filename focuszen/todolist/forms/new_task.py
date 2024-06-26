from django import forms
from ..models import TaskORMModel


class NewTaskForm(forms.ModelForm):
    class Meta:
        model = TaskORMModel
        fields = ['name', 'description', 'status', 'planned_effort', 'performer', 'actual_effort']
