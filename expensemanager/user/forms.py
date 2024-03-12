from django import  forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class ExpenseCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        #fields = UserCreationForm.Meta.fields + ('is_manager',)
        fields = ('username','first_name','last_name','email','phone_number','password1','password2')
        