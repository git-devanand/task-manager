from django.urls import path

from .views import TodoListView, TodoCreateView, TodoUpdateView, todo_delete, complete_todo, toggle_completed, AboutView, ProgressReportView

app_name = 'todo'

urlpatterns = [
    path('', TodoListView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('report/', ProgressReportView.as_view(), name='progress_report'),
    path('add/', TodoCreateView.as_view(), name='todo_add'),
    path('<int:pk>/update/', TodoUpdateView.as_view(), name='todo_update'),
    path('<int:pk>/delete/', todo_delete, name='todo_delete'),
    path('complete/<int:pk>/', complete_todo, name='todo_complete'),
    path('toggle/<int:pk>/', toggle_completed, name='todo_toggle'),
]