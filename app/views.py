from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def login_user(request):
    return render(request, 'login.html')

@login_required(login_url='')
def index(request):
    return render(request, 'index.html')

def logout_user(request):
    print(request.user)
    logout(request)
    return redirect('/')

@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/index.html')
        else:
            messages.error(request,'Usuário ou senha inválidos. Tentar novamente ou cadastre-se')
    return redirect('/')

        
