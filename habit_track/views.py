from django.shortcuts import render, redirect
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Habit, HabitCheck
from .forms import CreateHabitForm, DescriptionForm
from datetime import date, timedelta, datetime
import json, math, calendar

# Create your views here.
class HabitIndexPage(View, LoginRequiredMixin):
   template_name = "habit_tracks/index.html"
   context = {
      'monday': date.today() - timedelta(days=date.today().weekday())
   }

   def get(self, request):
      self.context['habits'] = Habit.objects.filter(user=request.user).order_by('-created_at').values()
      self.context['form'] = CreateHabitForm
      return render(request, self.template_name, self.context)

   def post(self, request):
      form = CreateHabitForm(request.POST, initial={'user': request.user})
      if form.is_valid():
         habit = form.save(commit=False)
         habit.user = request.user
         habit.save()

         message_dict = {
            'title': 'Habit To Track Created',
            'content': f'You can now track your habit ({form.cleaned_data["name"]}). Wish you all the best 🤞'
         }
         messages.success(request, json.dumps(message_dict))

         return redirect('Habit:main')

      self.context['form'] = form

      return render(request, self.template_name, self.context)

class HabitTrackingPage(DetailView, LoginRequiredMixin):
   template_name = 'habit_tracks/tracking_page.html'
   model = Habit
   slug_field = 'name'
   context_object_name = 'habit_tracked'
   start_time = None
   timeframe_type = None

   def get_start_date(self, start_date):
      arr = start_date.split('-')
      if len(arr) == 3:
         self.timeframe_type = 'Weekly'
         start_date = int(arr[2])
      else:
         self.timeframe_type = 'Monthly'
         start_date = 1

      return date(int(arr[0]), int(arr[1]), start_date)

   def get_queryset(self):
      querysets = super().get_queryset()
      # initial the start_time variable
      self.start_time = self.get_start_date(self.kwargs['start_date'])
      return querysets

   def get_weekly_menu(self, created_habit_time):
      # day index in template
      today_day_index = (6 - date.today().weekday())
      create_day_index = created_habit_time.weekday()

      # get created time and today
      start_day = created_habit_time - timedelta(days=create_day_index)
      end_day = date.today() + timedelta(days=today_day_index)
      total_week = ( (end_day - start_day).days + 1 ) // 7

      # returning monday and sunday time
      arr_result = []
      for i in range(0, total_week):
         arr_result.append({
            'monday': start_day + timedelta(days=(i*7)),
            'sunday': start_day + timedelta(days=( ((i+1)*7) - 1) )
         },)

      arr_result.reverse()
      
      return arr_result
   
   def get_monthly_menu(self, created_habit_time):
      # find year and month difference and total month difference
      year_difference = (date.today().year - created_habit_time.year)
      month_difference = (date.today().month - created_habit_time.month)
      total_month = year_difference * 12 + month_difference + 1

      # append all monthly menu
      arr_result = []
      for i in range(0, total_month):
         appended_year = created_habit_time.year + math.floor((created_habit_time.month + i) / 12)
         appended_month = created_habit_time.month + i
         # if it's more than 1 year
         while appended_month > 12:
            appended_month -= 12
         arr_result.append(date(appended_year, appended_month, 1))

      arr_result.reverse()

      return arr_result

   def get_today_index(self, get_type):
      if get_type == 'Weekly':
         start_time_timeframe = (date.today() - self.start_time).days
         if (start_time_timeframe ** 2) / 7 < 7:
            # set index in template
            return date.today().weekday()
         else:
            # no today index
            return 10
      elif get_type == 'Monthly':
         tday = date.today()
         if self.start_time.month != tday.month:
            return 100
         else:
            return tday.day - 1

   def get_checks_data(self, created_habit_time, habit, day_range):
      arr_result = []
      day_num_start = (self.start_time - created_habit_time).days + 1
      arr_result.append(day_num_start)
      arr_result.append(HabitCheck.objects.\
                              filter(habit=habit).\
                              filter(day_num__gte=day_num_start, day_num__lte=day_num_start + day_range).\
                              values_list('day_num', flat=True))
      arr_result.append(self.get_today_index(self.timeframe_type))

      return arr_result

   def get_current_timeframe(self, timeframe):
      if timeframe == 'Weekly':
         sunday_date = self.start_time + timedelta(days=6)
         from_date = self.start_time.strftime('%#d %B %Y')
         until_date = sunday_date.strftime('%#d %B %Y')
         return f"{from_date} - {until_date}"
      else:
         return self.start_time.strftime('%B %Y')

   def is_checked(self, habit):
      habit_create_time = date(habit.updated_at.year, habit.updated_at.month, habit.updated_at.day)
   
      if habit_create_time == date.today():
         return True
      else:
         return False



   def get_context_data(self, *args, **kwargs):
      kwargs = super().get_context_data(*args, **kwargs)
      habit = kwargs['habit_tracked']
      kwargs['timeframe_type'] = self.timeframe_type
      kwargs['today_timeframe'] = date.today() - timedelta(days=date.today().weekday())
      kwargs['is_checked'] = self.is_checked(habit)

      # get form
      kwargs['form'] = DescriptionForm(initial={
         'description': habit.description
      })

      # get the menu's
      kwargs['current_timeframe'] = self.get_current_timeframe(self.timeframe_type)
      create_time = habit.created_at
      created_habit_time = date(create_time.year, create_time.month, create_time.day)
      kwargs['weekly_menu'] = self.get_weekly_menu(created_habit_time)
      kwargs['monthly_menu'] = self.get_monthly_menu(created_habit_time)

      # get checks data
      if self.timeframe_type == 'Weekly':
         checks_data = self.get_checks_data(created_habit_time,  habit, 6)
      elif self.timeframe_type == 'Monthly':
         number_of_days_in_month = calendar.monthrange(self.start_time.year, self.start_time.month)[1]
         checks_data = self.get_checks_data(created_habit_time,  habit, number_of_days_in_month - 1)
      kwargs['day_num_start'] = checks_data[0]
      kwargs['habit_checks'] = checks_data[1]
      kwargs['today_day_index'] = checks_data[2]
      
      return kwargs
   
   def post(self, request, *args, **kwargs):
      form = DescriptionForm(request.POST)

      if form.is_valid():
         habit = Habit.objects.filter(name=kwargs['slug']).first()
         habit.description = form.cleaned_data['description']
         habit.save()
         
         message_dict = {
            'title': 'Habit Edited',
            'content': f'Description is successfully edited!'
         }
         messages.error(request, json.dumps(message_dict))
      else:
         message_dict = {
            'title': 'Edit Failed',
            'content': f'Description is not valid! Please re-check your input!'
         }
         messages.error(request, json.dumps(message_dict))

      
      return redirect('Habit:tracking_page', **kwargs)


class CheckHabit(View, LoginRequiredMixin):
   http_method_names = ['delete', 'post']

   def save_habit_checks(self, post_data, habit, habit_check, day_num):
      if 'check' in post_data:
         if not habit_check:
            new_check = HabitCheck(habit=habit, day_num=day_num)
            new_check.save()
            return True
      elif 'uncheck' in post_data:
         if habit_check:
            habit_check.delete()
            
      return False


   def save_habit_data(self, habit, day_num, habit_created_date):
      today_day_num = (date.today() - habit_created_date).days + 1
      if today_day_num == int(day_num):
         habit.updated_at = datetime.today()
         habit.save()
   
   def post(self, request, *args, **kwargs):
      day_num = request.POST['day_num']
      if int(day_num) >= 1:
         habit = Habit.objects.filter(user=request.user, name=kwargs['slug']).first()
         habit_created_date = date(habit.created_at.year, habit.created_at.month, habit.created_at.day)
         habit_check = HabitCheck.objects.filter(habit=habit, day_num=day_num).first()

         # create or delete habit checks
         if self.save_habit_checks(request.POST, habit, habit_check, day_num):
            message_dict = {
               'date': ( habit_created_date + timedelta(days=int(day_num)-1) ).strftime('%#d %B %Y')
            }
            messages.success(request, json.dumps(message_dict))

         # edit updated_at when we check on current date
         self.save_habit_data(habit, day_num, habit_created_date)
      else:
         message_dict = {
            'title': 'Check Failed',
            'content': f'Please try again!'
         }
         messages.error(request, json.dumps(message_dict))

      returned_start_time = date.today() - timedelta(days=date.today().weekday())
      if 'is_monthly' in request.POST:
         kwargs['start_date'] = returned_start_time.strftime('%Y-%m')
      else:
         kwargs['start_date'] = returned_start_time.strftime('%Y-%m-%d')
      return redirect('Habit:tracking_page', **kwargs)
      
         

      

   
   
