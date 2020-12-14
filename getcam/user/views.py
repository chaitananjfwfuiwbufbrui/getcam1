from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import  Profile
# Create your views here.
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from .forms import loginform,UserRegistrationForm,UserEditForm,ProfileEditForm
from django.contrib import messages
from django.views import View

from django.core.mail import send_mail

from django.urls import reverse
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
import base64
from .utils import token_Generator
# Create your views here.





    


# def index(request):
#     return render(request, "user/index.html")





# @login_required
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
                # emailcheck = User.objects.get(email = user_form.cleaned_data['email'])
                emailcheck = None
                print("checked")
                if emailcheck == None:
                    new_user = user_form.save(commit = False)
                    new_user.set_password(user_form.cleaned_data['password'])
                    new_user.is_active = False
                    new_user.save()
                    Profile.objects.create(user = new_user)
                    email = user_form.cleaned_data['email']
                    #domain knowing
                    print("a")
                    uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk)).encode()
                    # uidb64 = new_user.pk
                    print("b",uidb64,new_user.pk,type(uidb64))
                    domain = get_current_site(request).domain
                    link = reverse('activate',kwargs = {'uidb64':uidb64,'token':token_Generator.make_token(new_user)})
                    print("c")

                    #email verfication 
                    email_subject = 'verify your account'
                    activate_url = f'https://{domain}{link}'
                    email_message = f"hi  {new_user.username}  please verify your email address\n {activate_url} "
                    send_mail(
                        email_subject,
                        email_message,
                        'from@example.com',
                        [email],
                        fail_silently=False,
                    )
                    # email.SEND

                    messe = "Succesfully Account Created"
                    return render(request,'auth/register_done.html',{'new_user':new_user,'messe':messe})
                else:
                    messages.error(request,"account is already exist please try again")
                    errorr = True
                    messe = "Try Again with another email"
                    return render(request,'auth/register_done.html',{'errorr':errorr,'messe':messe})

            else:
                messages.error(request,"account is already exist please try again")
                errorr = True
                messe = "Try Again"
                return render(request,'auth/register_done.html',{'errorr':errorr,'messe':messe})
        else:
            user_form = UserRegistrationForm()
            
        # return render(request,'auth/register_done.html')
            return render(request,'auth/register.html',{'user_form' : user_form})
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance = request.user,data = request.POST)
        profile_form = ProfileEditForm(instance = request.user.profile,data = request.POST,files = request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            
            user_form.save()
            profile_form.save()
            messages.success(request,"Profile updated successfully")
            return render(request,'auth/dashboard.html',{'user_form':user_form,'profile_form':profile_form})
        else:
            messages.error(request,'Profile updated fail')

    else:
        user_form = UserEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance = request.user.profile)
    return render(request,'auth/edit.html',{'user_form':user_form,'profile_form':profile_form})




class verficationview(View):
    def get(self,request,uidb64,token):
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id = id)
        print(user,id)
        try:

            
            if not account_activation_token.check_token(user,token):
                messages.info(request,"emailverification already done!!")
                return redirect('login')
            if user.is_active:
                
                messages.info(request,"emailverified")
                return redirect('login')
            else:
                user.is_active = True
                user.save()
                messages.info(request,"emailverified")
        except Exception as ex :
            messages.info(request,"emailverification failed !!")


        
        return redirect('login')