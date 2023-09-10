from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date, timedelta, datetime
from .models import TimeTrack
from .forms import NewTimeTracks
import json

# Create your views here.
class TimeTrackView(View, LoginRequiredMixin):
   template_name = 'time_track/index.html'

   def proccess_date_url(self, monday_date):
      arr_date = monday_date.split('-')
      return date(int(arr_date[0]), int(arr_date[1]), int(arr_date[2]))

   def get(self, request, monday_date):
      date_url = self.proccess_date_url(monday_date)
      arr_result = []
      is_today_in_thisweek = False
      last_week = date_url - timedelta(days=7)
      next_week = date_url + timedelta(days=7)
      for x in range(0, 7):
         date_appended = date_url + timedelta(days=x)
         if date_appended == date.today():
            is_today_in_thisweek = True
            next_week = None
         arr_result.append({
            'date': date_appended,
            'tracks': [
               ('Productive', TimeTrack.objects.order_by('level').filter(date_for=date_appended, level="Productive")),
               ('Unproductive', TimeTrack.objects.order_by('level').filter(date_for=date_appended, level="Unproductive")),
               ('Neutral', TimeTrack.objects.order_by('level').filter(date_for=date_appended, level="Neutral"))
            ]
         })

      return render(request, self.template_name, {
         'time_tracks': arr_result,
         'is_today_in_thisweek': is_today_in_thisweek,
         'last_week': last_week,
         'next_week': next_week,
         'form': NewTimeTracks,
         'today_index': date.today().weekday()
      })


class DeleteTimeTrack(View, LoginRequiredMixin):
   model = TimeTrack

   def get(self, request, pk):
      self.model.objects.filter(id=pk).delete()
      monday_date = (date.today() - timedelta(days=date.today().weekday())).strftime('%Y-%m-%d')
      return redirect('TimeTrack:main', monday_date=monday_date)

class AddTimeTrack(View, LoginRequiredMixin):
   def post(self, request):
      form = NewTimeTracks(request.POST)
      if form.is_valid():
         time_track = form.save(commit=False)
         time_track.date_for = datetime.strptime(request.POST['date_for'], '%Y-%m-%d').date()
         time_track.save()

         message_dict = {
            'title': 'Track has been created',
            'content': f'Your track has been successfully added on ' + time_track.date_for.strftime('%#d %B %Y')
         }
         messages.success(request, json.dumps(message_dict))
      else:
         print(form.errors)
         message_dict = {
            'title': 'Track failed to be added',
            'content': f'Please try again and make sure everything is set perfectly'
         }
         messages.error(request, json.dumps(message_dict))

      monday_date = (date.today() - timedelta(days=date.today().weekday())).strftime('%Y-%m-%d')
      return redirect('TimeTrack:main', monday_date=monday_date)

