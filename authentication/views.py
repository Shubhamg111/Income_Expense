from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

from django.urls import reverse
from .utils import account_activation_token

from django.contrib.auth import authenticate,login,logout

from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
   
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading
# Create your views here.

class EmailThreading(threading.Thread):
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send(fail_silently = False)


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'email is Invalid'},status=400)
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error': 'email already exists. Choose another User.', 'available': True},status=400)
        return JsonResponse({'email_valid':True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric charaters', 'available': True},status=400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error': 'username already exists. Choose another User.', 'available': True},status=400)
        return JsonResponse({'username_valid':True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'auth/register.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context={
            'fieldValues':request.POST
        }

        if not User.objects.filter(username = username).exists():
            if not User.objects.filter(email = email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password should be at least 6 characters long')
                    return render(request, 'auth/register.html',context)
                
                user = User.objects.create_user(username = username,email = email)
                user.set_password(password)
                user.is_active = False
                user.save()


                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
              

               
                link = reverse('activate',kwargs = {"uidb64":email_body['uid'],"token":email_body['token']})
                
                email_subject = "Activate Your Account"
                activate_url = 'http://'+ current_site.domain + link
                
                email = EmailMessage(
                    email_subject,
                    'Hi ' + user.username + 'Please use this link to verify your Account\n' + activate_url,
                    "noreply@semicolon.com",
                    [email],
                   
                )
                EmailThreading(email).start()
                messages.success(request, 'Account created Successfully.')
                return render(request, 'auth/register.html')

        return render(request, 'auth/register.html')
    

class VerificationView(View):
    def get(self, request,uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login' + '?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated Successfully.')
            return redirect('login')


        except Exception as ex:
            pass
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request,'auth/login.html')
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password :
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request,'Welcome, '+user.username+' You are logged in.')
                    return redirect('add-expenses')
            

                messages.error(request,'Account is not active.please check your email')    
                return render(request,'auth/login.html')
            
            messages.error(request,'Invalid Credentials, try again.')    
            return render(request,'auth/login.html')
        messages.error(request,'Please Fill All Fields.')    
        return render(request,'auth/login.html')

class LogoutView(View):
    def post(self,request):
        logout(request)
        messages.success(request,"You have been logged Out.")
        return redirect('login')
    
class RequestPasswordResetEmail(View):
        def get(self,request):
            return render(request,'auth/reset-password.html')
    
        def post(self,request):
            email = request.POST['email']

            context={
                'values':request.POST
            }

            if not validate_email(email):
                messages.error(request,'Invalid Email')
                return render(request,'auth/reset-password.html')

            current_site = get_current_site(request)

            user=User.objects.filter(email=email)

            if user.exists():
                email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }
            

            
            link = reverse('reset-user-password',kwargs = {"uidb64":email_contents['uid'],"token":email_contents['token']})
            
            email_subject = "Password reset Instruction"
            reset_url = 'http://'+ current_site.domain + link
            
            email = EmailMessage(
                email_subject,
                'Hi there, Please use this link to reset your password\n' + reset_url,
                "noreply@semicolon.com",
                [email],
                
            )
            EmailThreading(email).start()

            messages.success(request,'We have sent you an email to reset your password.')
            return render(request, 'auth/reset-password.html', context)

 
class CompletePasswordReset(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        return render(request,'auth/set-new-password.html',context)
    
    def post(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        # password= request.POST['password']
        # password2= request.POST['password2']
        # if password != password2:
        #     messages.error(request,'Passwords do not match')
        #     return render(request,'auth/set-new-password.html',context)
        
        # if len(password)<6:
        #     messages.error(request,'Password should be at least 6 characters long')
        #     return render(request,'auth/set-new-password.html',context)
        

        # try:
        #     user_id=force_str(urlsafe_base64_decode(uidb64))
        #     user = User.objects.get(pk = user_id)
        #     user.password = password
        #     user.save()
        #     messages.success(request,'Password reset successfully, you can login with new password!')
        #     return redirect('login')

        # except Exception as identifier:
        #     messages.info(request,'Something Went Wrong.')
        #     return render(request,'auth/set-new-password.html',context)
        

        # Assuming `context` is defined if needed
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'auth/set-new-password.html', context)

        if len(password) < 6:
            messages.error(request, 'Password should be at least 6 characters long')
            return render(request, 'auth/set-new-password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)  # Use set_password to hash the password
            user.save()
            
            messages.success(request, 'Password reset successfully, you can log in with your new password!')
            return redirect('login')

        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return render(request, 'auth/set-new-password.html', context)

        except Exception as e:
            messages.error(request, 'Something went wrong.')
            return render(request, 'auth/set-new-password.html', context)




        
        # return render(request,'auth/set-new-password.html',context)
       
       
    




