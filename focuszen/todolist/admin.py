from django.contrib import admin

from todolist.models import TaskORMModel


# Register your models here.
@admin.register(TaskORMModel)
class TaskAdmin(admin.ModelAdmin):
    pass
