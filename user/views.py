from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.generic import View, RedirectView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from habit_track.models import Habit
from time_track.models import TimeTrack
from .forms import RegistrationForm, LoginForm
from datetime import date, timedelta
import json, math

# Create your views here.
class RegisterUser(View):
   template_name = 'user/register.html'
   context = {
      "form": RegistrationForm
   }

   def get(self, request):
      if request.user.is_authenticated:
         return redirect('Habit:main')
      return render(request, self.template_name, self.context)

   def post(self, request):
      form = RegistrationForm(request.POST)

      if form.is_valid():
         form.save()
         
         message_dict = {
            "title": "Account Created",
            "content": "Your account is successfully created, you can now log in!!"
         }
         messages.success(request, json.dumps(message_dict))

         return redirect('login')

      return render(request, self.template_name, {
         "form": form
      })

class LoginUser(View):
   template_name = "user/login.html"
   context = {
      "form": LoginForm
   }

   def get(self, request):
      if request.user.is_authenticated:
         return redirect('Habit:main')
      return render(request, self.template_name, self.context)

   def post(self, request):
      form = LoginForm(request.POST)

      if form.is_valid():
         
         # check if user is found with email
         user = User.objects.filter(email=form.cleaned_data['email']).first()
         if user is not None:
            # check if password is correct
            if check_password(form.cleaned_data['password'], user.password):
               login(request, user)

               message_dict = {
                  "title": "Logging In",
                  "content": "You have logged in to your account! Please enjoy the app."
               }
               messages.success(request, json.dumps(message_dict))

               return redirect('Habit:main')

         message_dict = {
            "title": "Login Error",
            "content": "Your email or password is incorrect. Please check your spelling!"
         }
         messages.error(request, json.dumps(message_dict))
         return redirect('login')

      return render(request, self.template_name, self.context)


class LogoutPage(RedirectView, LoginRequiredMixin):
   def get(self, request, *args, **kwargs):
      logout(request)

      message_dict = {
         "title": "Logout Successful",
         "content": "You have successfully logged out from this account!"
      }
      messages.success(request, json.dumps(message_dict))

      return redirect('login')


class ProfilePage(TemplateView, LoginRequiredMixin):
   template_name = "user/profile.html"

   def get_time_track(self, chart_type):
      time_track = None
      match chart_type:
         case "Today":
            time_track = TimeTrack.objects.filter(date_for=date.today())
         case "Last 7 Days":
            start_date = (date.today() - timedelta(days=6)).strftime('%Y-%m-%d')
            time_track = TimeTrack.objects.filter(date_for__range=[start_date, date.today().strftime('%Y-%m-%d')])
         case "Previous 7 Days":
            start_date = (date.today() - timedelta(days=13)).strftime('%Y-%m-%d')
            end_date = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
            time_track = TimeTrack.objects.filter(date_for__range=[start_date, end_date])
         case "Last 30 Days":
            start_date = (date.today() - timedelta(days=29)).strftime('%Y-%m-%d')
            time_track = TimeTrack.objects.filter(date_for__range=[start_date, date.today().strftime('%Y-%m-%d')])
         case "Previous 30 Days":
            start_date = (date.today() - timedelta(days=59)).strftime('%Y-%m-%d')
            end_date = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
            time_track = TimeTrack.objects.filter(date_for__range=[start_date, end_date])
      
      return time_track

   def process_progress(self, chart_type):
      time_track = self.get_time_track(chart_type)

      productive_time_spent = 0
      unproductive_time_spent = 0
      neutral_time_spent = 0
      for track in time_track:
         match track.level:
            case "Productive": 
               productive_time_spent += track.time
            case "Unproductive": 
               unproductive_time_spent += track.time
            case "Neutral": 
               neutral_time_spent += track.time
      total_time = productive_time_spent + unproductive_time_spent + neutral_time_spent
      if total_time == 0: total_time = 1
      unproductive_percentage = math.ceil((unproductive_time_spent / total_time) * 100)
      neutral_percentage = math.ceil((neutral_time_spent / total_time) * 100)
      productive_percentage = 100 - unproductive_percentage - neutral_percentage

      return {
         'type': chart_type,
         'productive_with_neutral': productive_percentage,
         'unproductive_with_neutral': unproductive_percentage,
         'productive_without_neutral': productive_percentage + (neutral_percentage / 2),
         'unproductive_without_neutral': unproductive_percentage + (neutral_percentage / 2),
         'neutral': neutral_percentage
      }
   
   def get(self, request):
      habits = Habit.objects.all()

      productivity_progress_type = ["Today", "Last 7 Days", "Previous 7 Days", "Last 30 Days", "Previous 30 Days"]
      productivity_progress = []
      for progress_type in productivity_progress_type:
         productivity_progress.append(self.process_progress(progress_type))

      context = {
         "habits": habits,
         "productivity_progress": productivity_progress,
         'monday': date.today() - timedelta(days=date.today().weekday())
      }
      
      return render(request, self.template_name, context)



      
