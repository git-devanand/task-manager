from django import forms
from django.utils import timezone

from .models import TodoItem

class TodoForms(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title', 'description', 'completed', 'priority', 'due_date', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        self.fields['due_date'].initial = tomorrow.date()
