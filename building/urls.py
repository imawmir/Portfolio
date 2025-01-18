from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="building_main"),
    path("buildings/", views.buildings, name="buildings"),
    path("buildings/<int:pk>/", views.building_info, name="building_info"),
    # path("spent/", views.spent, name="spent"),
    path("spent_update/", views.spent_update, name="spent_update"),
    path("spent/<int:pk>/", views.spent_info, name="spent_info"),
    path("sorted_spent/", views.sorted_spent, name="sorted_spent"),
    path("search_spent/", views.search_spent, name="search_spent"),
    path("excel/", views.generate_excel, name="generate_excel"),
    # path("user_login", views.user_login, name="user_login"),
    # path("user_logout", views.user_logout, name="user_logout")
]
