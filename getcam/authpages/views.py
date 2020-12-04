from django.shortcuts import render
from .models import  Profile
# Create your views here.
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from .forms import loginform,UserRegistrationForm
@login_required
def dashboard(request):
    return render(request,'auth/dashboard.html',{'section':'dashboard'})

def userlogin(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            cd  = form.cleaned_data
            user  = authenticate(request,username = cd['username'],password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse("authantication successfull")
                else:
                    return HttpResponse("disabled account")
            else:
                return HttpResponse("invalid login")
    else:
        form = loginform()
    return render(request,'auth/login.html',{'form':form})


def register(request):
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit = False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                Profile.objects.create(user = new_user)
                return render(request,'auth/register_done.html',{'new_user':new_user})
        else:
            user_form = UserRegistrationForm()
            
        # return render(request,'auth/register_done.html')
            return render(request,'auth/register.html',{'user_form' : user_form})
        