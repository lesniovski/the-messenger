from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AuthUser
from datetime import datetime

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

@csrf_protect
def submit_register(request):
    data = {}
    data['msg'] = []
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rpassword = request.POST.get('rpassword')
        is_superuser = False
        is_staff = True
        is_active = True
        date_joined = datetime.now()
        try:
            val_username = User.objects.filter(username=username)
            val_email = User.objects.filter(email=email)
            if (len(val_username) > 0):
                data['msg'].append('usuário já cadastrado!')
                print("teste")
                x = 1
            if (len(val_email) > 0):
                data['msg'].append('E-mail já cadastrado!')
                x = 1
        except:
            data['msg'].append('Erro ao verificar usuário ou email!')
            return render(request, 'register.html', data)
        
        if (password != rpassword):
            data['msg'].append('Senhas não conferem')
            x = 1
        if (x > 0):
            return render(request,'register.html', data)
        try:
            user = User(is_superuser=is_superuser,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            date_joined=date_joined)
            user.set_password(password)
            user.save()
            data['msg'].append('Cadastro realizado com Sucesso!')
            return render(request, 'login.html', data)
        except:
            data['msg'].append('Ocorreu algum erro, tente novamente mais tarde!')
            return render(request,'register.html', data)
    else:
        return render(request, 'register.html', data)

def register(request):
    print("teste register")
    return render(request, 'register.html')        

@csrf_protect
def recovery_pass(request):
    return render(request, 'recovery_pass.html')