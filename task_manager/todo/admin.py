from django.contrib import admin

from .models import Category, TodoItem
# Register your models here.
admin.site.register(TodoItem)
admin.site.register(Category)
