from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.views.generic import TemplateView
from django.db.models import Count
from django.utils import timezone
from .models import TodoItem
from .forms import TodoForms

# Create your views here.
class TodoListView(ListView):
    model = TodoItem
    template_name = 'todo/home.html'
    context_object_name = 'todos'
    ordering = ['priority']
    


class TodoCreateView(CreateView):
    model = TodoItem
    template_name = 'todo/todo_form.html'
    form_class = TodoForms
    success_url = reverse_lazy('todo:home')

    def form_valid(self, form):
        return super().form_valid(form)    

class TodoUpdateView(UpdateView):
    model = TodoItem
    template_name = 'todo/todo_form.html'
    form_class = TodoForms
    success_url = reverse_lazy('todo:home')

    def form_valid(self, form):
        return super().form_valid(form) 
    


def todo_delete(request, pk):
    TodoItem.objects.filter(pk=pk).delete()
    return redirect('todo:home')

def complete_todo(request, pk):
    todo = TodoItem.objects.get(pk=pk)
    todo.completed = True
    todo.save()
    return redirect('todo:home')

def toggle_completed(request, pk):
    todo = TodoItem.objects.filter(pk=pk).get()
    todo.completed = False
    todo.save()
    return redirect('todo:home')

class AboutView(TemplateView):
    template_name = 'todo/about.html'



class ProgressReportView(TemplateView):
    template_name = 'tasks/progress_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve tasks that were created or completed in the past 7 days
        start_date = timezone.now() - timezone.timedelta(days=7)
        tasks = TodoItem.objects.filter(
            created_at__gte=start_date
        ).annotate(
            day=Count('id', distinct=True, output_field=models.DateField()),
            is_completed=Count('id', filter=models.Q(is_completed=True), distinct=True)
        ).values('day', 'is_completed')

        # Convert queryset to a list of dictionaries
        task_data = []
        for task in tasks:
            task_data.append({
                'day': task['day'].strftime('%Y-%m-%d'),
                'completed': task['is_completed'],
                'not_completed': task['day'] - task['is_completed']
            })

        # Add task data to context
        context['task_data'] = task_data

        return context
