from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='pump_main'),
    path('menu/', views.menu, name='menu'),
    path('submersible/', views.submersible, name='submersible'),
    path('submersible_pipe_num/', views.submersible_pipe_num, name='submersible_pipe_num'),
    path('submersible_oft/', views.submersible_oft, name='submersible_oft'),
    path('highpressure/', views.highpressure, name='highpressure'),
    path('highpressure_pipe_num/', views.highpressure_pipe_num, name='highpressure_pipe_num'),
    path('highpressure_oft/', views.highpressure_oft, name='highpressure_oft'),
    path('submersible_calculation/', views.submersible_calculation, name='submersible_calculation'),
    path('highpressure_calculation/', views.highpressure_calculation, name='highpressure_calculation'),
]


    