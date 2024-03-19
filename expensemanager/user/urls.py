from django.contrib import admin
from django.urls import path,include
from .views import ExpenseRegisterView,UserLoginView,logout_view,ExpenseDashboardView
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth import logout

urlpatterns = [
    
    path('expense_register/',ExpenseRegisterView.as_view(),name='expense_register'),
    path("login/",UserLoginView.as_view(),name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('expense_dashboard/',ExpenseDashboardView.as_view(),name='expense_dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    

    
]