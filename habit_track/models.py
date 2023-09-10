from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Habit(models.Model):
   name         = models.CharField(max_length=100)
   description  = models.TextField()
   habit_type   = models.CharField(max_length=50)
   updated_at   = models.DateTimeField(default=datetime.today())
   created_at   = models.DateTimeField(auto_now_add=True)
   user         = models.ForeignKey(User, on_delete=models.CASCADE)

   def __str__(self):
      return f"{self.name} ({self.habit_type})"

class HabitCheck(models.Model):
   day_num = models.IntegerField()
   habit = models.ForeignKey(Habit, on_delete=models.CASCADE)

   def __str__(self):
      return f"Day {self.day_num}, {self.habit.name} | {self.habit.user.username}"
   
