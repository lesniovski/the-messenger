from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AuthUser, UserFriend
from datetime import datetime
from app import emailService
from random import randint

# Create your views here.


def login_user(request):
    return render(request, 'login.html')

@login_required(login_url='')
def index(request):
    data = {}
    data['user'] = []
    data['users'] = []
    data['user'].append(request.user)
    data['friends'] = UserFriend.objects.filter(my_id=request.user.id)
    #data['friends'] = UserFriend.objects.filter(friend_id=request.user.id)

    if request.method == 'POST':
        var = request.POST.get('buscar')
        data['users'] = AuthUser.objects.filter(username__contains=var).exclude(
            id=request.user.id).exclude(userfriend__in=data['friends'])
        #for i in data['friends']:
        #    userRemove = AuthUser.objects.get(id=i.friend_id.id)
        #    for j in users:
        #        if (j == userRemove):
        #            del(users[j])
        #    print(userRemove)
        #    print(i.friend_id.username)
        #selected_related
        #users = AuthUser.objects.filter(username__contains=var).exclude(id=request.user.id).exclude(id=data['friends'][i].UserFriend.friend_id)
        #auxUsers = UserFriend.objects.filter(friend_id(username__contains=var))
        #for i in auxUser:
        #    for j in users:
        #        if(auxUsers[i].friend_id.id == users[j].AuthUser.id):
        #            users[j].remove
        #for i in users:
        #    data['users'].append(i)
    return render(request, 'index.html', data)

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
            return redirect('index.html')
        else:
            messages.error(request,'Usuário ou senha inválidos. Tentar novamente ou cadastre-se')
    return redirect('/')

@csrf_protect
def submit_register(request):
    data = {}
    data['msg'] = []
    x = 0
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
    return render(request, 'register.html')        

@csrf_protect
def recovery_pass(request):
    data = {}
    data['msg'] = []
    data['error'] = []
    if request.method =='POST':
        email = request.POST.get('email')
        try:
            if(email == ''):
                data['error'].append('email inválido')
            else:
                val_user = User.objects.filter(email=email)
                if (len(val_user) > 0):
                    newpass = randint(10000000,99999999)
                    user = User.objects.get(email=email)
                    user.set_password(newpass)
                    user.save()
                    emailService.recoveryPass(newpass, user.username, email)
                    data['msg'].append('Sua nova senha foi enviada no email!')
                else:
                    data['error'].append('email não cadastrado!')   
        except:
            data['error'].append('Ocorreu algum erro, tente novamente mais tarde!')
            return render(request,'recovery_pass.html', data)  
    return render(request, 'recovery_pass.html', data)

@csrf_protect
def friend(request):
    data = {}
    #data['user'] = []
    #data['users'] = []
    #data['user'].append(request.user)
    #data['friends'] = []
    data['error'] = []
    if request.method == 'GET':
        id = request.GET.get('id')
        op = request.GET.get('op')
        if(id != None and op != None):
            try:           
                friend = AuthUser.objects.get(id=id)
                iduser = int(request.user.id)
                #x = UserFriend.objects.filter(my_id=iduser,friend_id=friend)
                if(friend == ''):
                    data['error'].append('Amigo inválido')
                #elif(x[0].friend_id == friend):
                #    data['error'].append('Amigo já adicionado')
                #    return redirect(request, 'index', data)
                elif(op == "add"):
                    fr = UserFriend(my_id=iduser,friend_id=friend)
                    fr.save()
                elif(op == "del"):
                    fr = UserFriend.objects.get(my_id=iduser,friend_id=friend)
                    fr.delete()
            except:
                data['error'].append("Erro ao adicionar amigo! Tente novamente")
        return redirect('index')