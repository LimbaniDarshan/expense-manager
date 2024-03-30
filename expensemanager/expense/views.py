from typing import Any
from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.views.generic import ListView
from .models import Expense,Books,ExpenseGoal
from .forms import AddExpenseForm,BookCreationForm,GoalForms
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user.models import User
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Expense
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
from django.db.models import Sum
from django.urls import reverse
from django.views import View
from collections import defaultdict
from django.contrib import messages
import datetime
from django.db.models.functions import TruncMonth  # Import TruncMonth

@login_required
def expense_report(request):
    # Get expenses for the logged-in user and group by month
    expenses_by_month = Expense.objects.filter(user=request.user).annotate(
        month=TruncMonth('expDateTime')
    ).values('month').annotate(total_amount=Sum('amount')).order_by('month')

    return render(request, 'expense/report.html', {'expenses_by_month': expenses_by_month})

class ExpenseCreationView(CreateView):
    template_name = 'expense/create.html'
    model = Expense
    form_class = AddExpenseForm
    success_url = '/expense/list/'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter the 'goal' field queryset based on the logged-in user
        form.fields['goal'].queryset = form.fields['goal'].queryset.filter(user=self.request.user)
        return form
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # Assigning the logged-in user to the 'user' field
        expense = form.save(commit=False) 
        
        if expense.goal:
            # Check if the expense amount exceeds the maximum amount of the goal
            if expense.amount > expense.goal.maxAmount:
                messages.error(self.request, "Expense amount exceeds the maximum amount allowed for this goal.")
                return super().form_invalid(form)
            else:
                # Deduct the expense amount from the remaining amount of the goal
                expense.goal.maxAmount -= expense.amount
                expense.goal.save()
                messages.success(self.request, "Expense added successfully. Amount deducted from the goal.")
        
        expense.save()

        messages.success(self.request, "Expense added successfully.")
        return super().form_valid(form)
    



    
@method_decorator(login_required, name='dispatch')
class ExpenseListView(ListView):
    template_name = 'expense/list.html'
    model = Expense
    context_object_name = 'expenses'

    def get_queryset(self):
        # Get the logged-in user
        user = self.request.user
        # Filter expenses based on the logged-in user
        queryset = super().get_queryset().filter(user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate total sum of amounts
        total_amount = self.get_queryset().aggregate(Sum('amount'))['amount__sum']
        context['total_amount'] = total_amount if total_amount else 0
        # return context
        
        expenses_by_category = defaultdict(list)
        for expense in context['expenses']:
            expenses_by_category[expense.category.categoryName].append(expense)
        
        # Calculate total sum of amounts for each category
        total_amount_by_category = {}
        for category, expenses in expenses_by_category.items():
            total_amount_by_category[category] = sum(expense.amount for expense in expenses)
        
        context['categories'] = expenses_by_category.keys()
        context['expenses_by_category'] = expenses_by_category 
        context['total_amount_by_category'] = total_amount_by_category if total_amount_by_category else 0
        return context
 
class ExpenseDetailView(DetailView):
    model = Expense
    context_object_name = "expensee"
    template_name = "expense/expense_detail.html"
    
class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = AddExpenseForm
    success_url = "/expense/list/"
    template_name = "expense/expense_update.html" 
    
class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = "expense/expense_delete.html"    
    success_url = "/expense/list/"
    



    

def pieChart(request):
    labels =[]
    data =[]
    
    queryset = Expense.objects.order_by('-amount')[:7]  
    print(queryset)
    
    for expense in queryset:
        labels.append(expense.category.categoryName)  # Accessing the categoryName through the ForeignKey
        print(labels)
        data.append(expense.amount)
        
    return render(request, 'expense/pie_chart.html',{
        'labels':labels,
        'data':data
    })      


class BookCreateView(CreateView):
    model = Books
    template_name = 'expense/create_book.html'
    success_url = '/expense/list/'
    form_class = BookCreationForm
        
class BookListView(ListView):
    template_name = 'expense/book_list.html'
    model = Books
    context_object_name = 'books'       
    
class ExpenseGoalView(CreateView):
    template_name='expense/goal.html'
    model = ExpenseGoal
    forms_class = GoalForms
    success_url = '/expense/listgoal/'
    fields = ['goalName','maxAmount','startDate','endDate','status']
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if user is not authenticated
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associate the current user with the created goal
        return super().form_valid(form)
    
class GoalListListView(ListView):
    template_name = 'expense/listgoal.html'
    model = ExpenseGoal
    context_object_name = 'goal'
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if user is not authenticated
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        # Filter goals based on the logged-in user
        return ExpenseGoal.objects.filter(user=self.request.user)
    
class GoalUpdateView(UpdateView):
    model = ExpenseGoal
    form_class = GoalForms
    success_url = "/expense/listgoal/"
    template_name = "expense/goal_update.html"

class GoalDeleteView(DeleteView):
    model = ExpenseGoal
    success_url = "/expense/listgoal/"
    template_name = "expense/goal_delete.html"
    
    
class UpdateStatusView(View):
    
    def post(self, request, pk):
        # Get the task instance
        print("pk....",pk)
        mode = Expense.objects.get(id=pk)
        print("task....",mode)
        
        # Check the current status and update it accordingly
        if mode.status == "uncleared":
            mode.status = "cleared"
        elif mode.status == "cleared":
            mode.status = "uncleared"
        else:
            mode.status = "cleared"    
        
        
        # Save the updated task
        mode.save()
        
        return redirect(reverse('expense_list')) #lazy reverse
    
class GoalUpdateStatusView(View):
    
    def post(self, request, pk):
        # Get the goal instance
        goal = ExpenseGoal.objects.get(id=pk)
        
        # Check the current status and update it accordingly
        if goal.status == "not-active":
            goal.status = "active"
        elif goal.status == "active":
            goal.status = "paused"
        else:
            goal.status = "not-active"
        
        # Save the updated goal
        goal.save()
        
        return redirect(reverse('listgoal'))  # Redirect to the goal list page after updating the status
    
    
def barChart(request):
    labels =[]
    data =[]
    
    queryset = Expense.objects.order_by('-amount')[:8]  
    print(queryset)
    
    
    for expense in queryset:
        labels.append(expense.category.categoryName)  # Accessing the categoryName through the ForeignKey
        print(labels)
        data.append(expense.amount)
        print(data)
        
    return render(request, 'expense/chart.html',{
    'labels':labels,
    'data':data
    })  