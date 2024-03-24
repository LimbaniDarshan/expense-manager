from django.shortcuts import render,redirect
from django.views.generic import CreateView,DeleteView,DetailView
from .models import User
from .forms import ExpenseCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import ListView
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponseRedirect
from typing import Any
from django.forms.models import BaseModelForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from expense.models import Expense
from django.contrib.auth import login
from .forms import *
# Create your views here.

class ExpenseRegisterView(CreateView):
    model = User
    form_class = ExpenseCreationForm
    template_name = 'user/expense_register.html'
    success_url = '/user/login/'
    
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # Assigning the logged-in user to the 'user' field
        return super().form_valid(form)
    
class UserLoginView(LoginView):  
    template_name = 'user/login.html' 
    model = User  
    
    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.username:
                return '/user/expense_dashboard/'
            else:
                return '/expense/expense_register/'
            
def logout_view(request):
    logout(request)
    return redirect('index')

@method_decorator(login_required, name='dispatch')
class ExpenseDashboardView(ListView):
    def get(self, request, *args, **kwargs):
        #logic to get all the projects
        context ={}
        expenses = Expense.objects.filter(user=self.request.user)
        labels = [expense.category.categoryName for expense in expenses]
        data = [expense.amount for expense in expenses]
        print(labels)
        # context['labels'] = labels
        # context['data'] = data
        
        return render(request, 'user/expense_dashboard.html',{
            "data":data,
            "labels":labels
        })
    
    template_name = 'user/expense_dashboard.html' 
    
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')  # Redirect to the profile page after saving
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'user/edit_profile.html', {'form': form})
    

    