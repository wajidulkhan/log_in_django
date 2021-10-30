
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm 
from django.contrib.auth.models import User




class SignUpFrom(UserCreationForm): 
    class Meta:
        model= User
        fields = ['username', 'first_name','last_name','email'] 

class viewsign(UserChangeForm): 
    class Meta:
        model= User
        fields = ['username', 'first_name','last_name','email','date_joined','last_login','is_active']  
        labels = {'email':'Email'}  

class editadmin(UserCreationForm): 
    class Meta:
        password = None 
        model= User
        fields = '__all__' 
        labels = {'email':'Email'}  