from django import forms
from .models import Habit

class CreateHabitForm(forms.ModelForm):
   class Meta:
      model = Habit
      fields = ['name', 'description', 'habit_type']
      widgets = {
         'name': forms.TextInput(attrs={
            'class': 'w-full bg-transparent border border-slate-600 rounded-sm mt-2 mb-1 p-2 text-sm outline-none'
         }),
         'description': forms.Textarea(attrs={
            'class': 'w-full bg-transparent border border-slate-600 rounded-sm mt-2 mb-1 p-2 text-sm outline-none resize-none',
            'rows': 5
         }),
         'habit_type': forms.TextInput(attrs={
            'class': 'hidden'
         }),
      }

class DescriptionForm(forms.ModelForm):
   class Meta:
      model = Habit
      fields = ['description']
      widgets = {
         'description': forms.Textarea(attrs={
            'class': 'w-2/3 block bg-transparent border border-slate-600 rounded-sm mt-2 mb-1 p-2 text-sm outline-none resize-none',
            'rows': 5
         })
      }
