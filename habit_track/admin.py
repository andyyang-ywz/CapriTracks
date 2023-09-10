from django.contrib import admin

# Register your models here.
from .models import Habit, HabitCheck

class HabitAdmin(admin.ModelAdmin):
   readonly_fields = ['updated_at', 'created_at']


admin.site.register(Habit, HabitAdmin)
admin.site.register(HabitCheck)
