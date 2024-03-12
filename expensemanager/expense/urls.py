from django.contrib import admin
from django.urls import path,include
from .views import *
from .import views


urlpatterns = [
    path("create/",ExpenseCreationView.as_view(),name='expense_create'),
    path("list/",ExpenseListView.as_view(),name='expense_list'),
    path("detail/<int:pk>/",ExpenseDetailView.as_view(),name="detail_expense"),
    path("delete/<int:pk>/",ExpenseDeleteView.as_view(),name="delete_expense"),
    path("update/<int:pk>/",ExpenseUpdateView.as_view(),name="update_expense"),
    
    path ("chart/",views.pieChart,name="chart"),
    
    path("book_create/",BookCreateView.as_view(),name="book_create"),
    path("book_list/",views.BookListView.as_view(),name="book_list"),
    
    path("goal/",ExpenseGoalView.as_view(),name="goal"),
    path("listgoal/",GoalListListView.as_view(),name="listgoal"),
    path("goalStatus_update/<int:pk>/",views.GoalUpdateStatusView.as_view(),name="update_goalstatus"),

    
    path("status_update/<int:pk>/",views.UpdateStatusView.as_view(),name="update_status"),

    
]