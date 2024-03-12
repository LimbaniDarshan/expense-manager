from django import forms
from .models import Expense,Books,ExpenseGoal
import django.forms.utils
import django.forms.widgets
class AddExpenseForm(forms.ModelForm):
    
    class Meta:
        model = Expense
        exclude = ['user']  # Exclude the 'user' field from the form
        widgets = {
            'expDateTime': forms.DateInput(attrs={'type': 'date'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['goal'].required = False    
        
class BookCreationForm(forms.ModelForm):
    class Meta:
        model = Books
        fields ='__all__'
        
class GoalForms(forms.ModelForm):
    
    class Meta:
        model = ExpenseGoal
        fields = '__all__'
        widgets = {
            'startDate': forms.DateInput(attrs={'type': 'date'}),
            'endDate': forms.DateInput(attrs={'type': 'date'})
        }
        