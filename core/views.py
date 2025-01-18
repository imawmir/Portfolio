from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import WorkSample, Client


# Index
def index(request):
    worksamples = WorkSample.objects.all()
    try:
        client = get_object_or_404(Client, user=request.user)
        return render(request, 'index.html', {'worksamples': worksamples, "client": client})
    except:
        return render(request, 'index.html', {'worksamples': worksamples})


# User Profile
def profile(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, "profile.html", {"client": client})


# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, "Logged In Successfully")
            return redirect('index')
        messages.info(request, "Login Failed, Please Try Again")
    return render(request, 'login.html')


# Register
def user_register(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # print(username,email,phone)
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                print('username exists!')
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request, "Email already exists")
                    print("Email exists!")
                else:
                    user = User.objects.create_user(
                        username=username, 
                        email=email, 
                        password=password)
                    user.save()
                    data = Client(user=user, phone=phone, image=image)
                    data.save()        
            
                    # Login after Registration
                    new_user = authenticate(username=username, password=password)
                    if new_user is not None:
                        login(request, user)
                        return redirect('index')
        else:
            messages.info(request, "Password and Confirm password Mismatch")
            return redirect('register')
            
    return render(request, 'register.html')


# Logout
def user_logout(request):
    logout(request)
    return redirect('index')
