from django.db import models

# Create your models here.
class TimeTrack(models.Model):
   PRODUCTIVITY_LEVEL = [("Productive", "Productive"), ("Unproductive", "Unproductive"), ("Neutral", "Neutral")]
   time = models.PositiveIntegerField()
   name = models.CharField(max_length=50)
   level = models.CharField(choices=PRODUCTIVITY_LEVEL, max_length=20)
   date_for = models.DateField(default=None)

   def __str__(self):
      hour = self.time // 60
      minutes = self.time % 60
      return f"{self.name} | {hour} hour {minutes} minutes | {self.level}"
   
