from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video', views.video_home, name='video'),
    path('check_crash', views.check_crash_video, name='check_crash'),
    path('check_fire', views.check_fire, name='check_fire'),
    path('check_damage', views.check_damage, name='check_damage'),
    path('image', views.image_home, name='image'),
]