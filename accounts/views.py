from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User

from contacts .models import Contact
# Create your views here.

def register(request):
    if request.method == 'POST':
        #register user
        # messages.error(request,'Testing error messages')
        #GET FORM VALUES
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            #check username 
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username taken')
                return redirect('accounts:register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Email taken')
                    return redirect('accounts:register')
                else:
                    user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                    #login after register 
                    # auth.login(request,user)
                    # messages.success(request,'You are logged id')
                    # return redirect('pages:index')
                    user.save()
                    messages.success(request,'Registered Successfully !!! ')
                    return redirect('accounts:login')
        else:
            messages.error(request,'Password do not match')
            return redirect('accounts:register')
        return redirect('accounts:register')

    return render(request,'accounts/register.html')

def login(request):
    if request.method == 'POST':
        #login user
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are logged In')
            return redirect('accounts:dashboard')

        messages.error(request,'Invalid Credentials')
        return redirect('accounts:login')

    return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'Successfully Logout')
        return redirect('pages:index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts':user_contacts
    }
    return render(request,'accounts/dashboard.html',context)