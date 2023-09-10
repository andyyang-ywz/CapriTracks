from django import forms
from.models import TimeTrack

class NewTimeTracks(forms.ModelForm):
   class Meta:
      model = TimeTrack
      fields = ['name', 'level', 'time']
      widgets = {
         'name': forms.TextInput(attrs={
            'class': 'block w-[400px] bg-transparent border border-slate-700 rounded-sm p-2 text-sm outline-none',
         }),
         'time': forms.NumberInput(attrs={
            'class': 'block w-[400px] bg-transparent border border-slate-700 rounded-sm p-2 text-sm outline-none',
         }),
         'level': forms.HiddenInput()
      }