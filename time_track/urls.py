from django.urls import path, reverse_lazy
from .views import TimeTrackView, DeleteTimeTrack, AddTimeTrack

app_name = "TimeTrack"
urlpatterns = [
   path('delete_track/<pk>/', DeleteTimeTrack.as_view(), name='delete'),
   path('add_track/', AddTimeTrack.as_view(), name='add'),
   path('<monday_date>/', TimeTrackView.as_view(), name='main'),
]