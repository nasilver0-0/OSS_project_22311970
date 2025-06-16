from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),                                                                                  
    path('register/', views.register_view, name='register'),
    path('add_ingredient/', views.add_ingredient_view, name='add_ingredient'),
    path('record_meal/', views.record_meal_view, name='record_meal'),
    path('meal_stats/', views.meal_stats_view, name='meal_stats'),
    path('settings/', views.settings_view, name='settings'),
    path('delete_ingredient/<int:pk>/', views.delete_ingredient_view, name='delete_ingredient'),
    path('meal/<str:ymd>/', views.meal_detail_view, name='meal_detail'),
]