from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from .forms import SignUpFrom,viewsign,editadmin
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash  
from django.contrib.auth.models import User
# Create your views here.
#sign up
def SignUp(request):
    if request.method =='POST':
        fm = SignUpFrom(request.POST) 
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/login/') 
    else:
        fm=SignUpFrom()
    return render(request, 'enroll/signup.html', {'form':fm}) 

#login
def log(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password'] 

                user = authenticate(request, username=uname, password=upass) 

                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/profile/') 
        else:
           fm = AuthenticationForm() 
        return render(request, 'enroll/index.html', {'form': fm}) 
    else:
       return HttpResponseRedirect('/profile/')
# def log(request): 
#     username = request.POST.get('username')
#     password = request.POST.get('password') 
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         return HttpResponseRedirect('/profile/') 
          
     

def profile(request):
    if request.user.is_authenticated:       
        if request.method == 'POST':
            if request.user.is_superuser == True:
                fm = editadmin(request.POST, instance=request.user)
                print(fm) 
                users = User.objects.all() 
            else:
                fm = viewsign(request.POST, instance=request.user) 
                print(fm) 
            if fm.is_valid():
                fm.save()
        else:
            users = None
            if request.user.is_superuser == True:
                users = User.objects.all() 
                fm = editadmin(instance=request.user)
                print(users)  

            else: 
                fm = viewsign(instance=request.user) 
        return render(request, 'enroll/profile.html',{'name':request.user ,'form': fm, 'user': users}) 
    else:
        return HttpResponseRedirect('/login/') 


#logout    
def log_out(request):
    logout(request) 
    return HttpResponseRedirect('/login/') 


#chanage password
def change_pass(request):
    if request.user.is_authenticated: 
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user) 
                return HttpResponseRedirect('/profile/') 
        else:
            fm = PasswordChangeForm(user=request.user) 
        return render(request, 'enroll/change.html',{'form':fm} ) 
    else:
        return HttpResponseRedirect('/login/') 


#user profile check in superuser
def userprofile(request, id):
    if request.user.is_authenticated: 
        sm = User.objects.get(pk=id)
        fm = editadmin(instance=sm)
        return render(request, 'enroll/userprofile.html', {'form': fm}) 
    else:
        return HttpResponseRedirect('/login/') 