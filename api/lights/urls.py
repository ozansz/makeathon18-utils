from django.urls import path, include

from lights.views import *

urlpatterns = [
    path('token/<int:id>/', TokenView.as_view()),
    path('data/sensor/', SensorView.as_view()),
    path('data/cam/', CamView.as_view()),
    path('timing/', TimingView.as_view()),
]
