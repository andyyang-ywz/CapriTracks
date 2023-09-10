from django.urls import path
from django.views.generic import TemplateView
from .views import HabitIndexPage, HabitTrackingPage, CheckHabit

app_name = "Habit"
urlpatterns = [
   path('', HabitIndexPage.as_view(), name="main"),
   path('<str:username>/<str:slug>/check_habit', CheckHabit.as_view(), name='check_habit'),
   path('<str:username>/<str:slug>/<start_date>', HabitTrackingPage.as_view(), name="tracking_page")
]