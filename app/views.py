from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AuthUser, UserFriend, MessagesFriend
from datetime import datetime
from app import emailService
from random import randint
from django.db.models import Q

# Create your views here.


def login_user(request):
    return render(request, 'login.html')

@login_required(login_url='')
def index(request):
    try:
        data = {}
        data['user'] = []
        data['users'] = []
        data['user'].append(request.user)
        user = AuthUser.objects.get(id=request.user.id)
        data['friends'] = UserFriend.objects.filter(my_id=request.user.id, status="C")
        data['friendsP'] = UserFriend.objects.filter(friend_id=user, status="A",analyzed=False)
        data['friendsAG'] = UserFriend.objects.filter(my_id=request.user.id, status="A", analyzed=False)
        data['friendsPA'] = []
        for item in data['friendsP']:
            friend = AuthUser.objects.get(id=item.my_id)
            data['friendsPA'].append(friend)
        data['friendsA'] = UserFriend.objects.filter(my_id=request.user.id,status="C",analyzed=False)
        data['friendsR'] = UserFriend.objects.filter(my_id=request.user.id,status="R",analyzed=False)

        if request.method == 'POST':
            var = request.POST.get('buscar')
            data['users'] = AuthUser.objects.filter(username__contains=var).exclude(
                id=request.user.id).exclude(userfriend__in=data['friends'])
        
        if request.method == 'GET':
            id = request.GET.get('id')
            op = request.GET.get('op')
            friend = AuthUser.objects.get(id=id)
            if(id != None and op != None):
                fr = UserFriend.objects.filter(my_id=request.user.id,friend_id=friend)
                if (op == "ok"):
                    for item in fr:
                        item.analyzed = True
                        item.save()
                elif(op == "okR"):
                    for item in fr:
                        item.delete()
            else:
                data['msg'] = ('Erro ao confirmar informações de amizade')
    except:
            data['msg'] = ('Erro ao verificar carregar dados!')
            return render(request, 'index.html', data)

    return render(request, 'index.html', data)

def logout_user(request):
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
            return redirect('index')
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
    data['error'] = []
    if request.method == 'GET':
        id = request.GET.get('id')
        op = request.GET.get('op')
        if(id != None and op != None):
            try:           
                user = AuthUser.objects.get(id=request.user.id)
                friend = AuthUser.objects.get(id=id)
                iduser = int(request.user.id)
                if(friend == ''):
                    data['error'].append('Amigo inválido')
                elif(op == "add"):
                    fr = UserFriend(my_id=iduser,friend_id=friend,status="A",analyzed=False)
                    fr.save()
                elif(op == "del"):
                    fr = UserFriend.objects.filter(my_id=iduser,friend_id=friend)
                    for item in fr:
                        item.delete()
                elif(op == "apr"):
                    fra = UserFriend.objects.filter(my_id=id, friend_id=user)
                    for item in fra:
                        item.status = "C"
                        item.analyzed = False
                        item.save()
                    fr = UserFriend(my_id=iduser,friend_id=friend,status="C",analyzed=True)
                    fr.save()
                elif(op == "rec"):
                    fra = UserFriend.objects.filter(my_id=friend.id, friend_id=user)
                    for item in fra:
                        item.status = "R"
                        item.analyzed = False
                        item.save()
            except:
                data['error'].append("Erro ao adicionar amigo! Tente novamente")
        return redirect('index')

@csrf_protect
def messagesP(request):
    print("Passei aqui")
    data = {}
    data['messages'] = []
    data['users'] = []
    data['erro'] = []
    if request.method == 'GET':
        id = request.GET.get('id')
        op = request.GET.get('op')
        if(id != None and op != None):
            try:           
                user = AuthUser.objects.get(id=request.user.id)
                friend = AuthUser.objects.get(id=id)
                iduser = int(request.user.id)
                data['messages'] = get_messages(iduser, friend)
                data['users'].append(friend)
            except:
                data['erro'].append("Erro ao carregar mensagens! Tente novamente")
    return render(request, 'messages.html', data)
    #return redirect('index', {'messages': data})

def get_messages(iduser, friend):
    try:
        idm1 = UserFriend.objects.get(my_id=iduser, friend_id=friend)
        user = AuthUser.objects.get(id=iduser)
        idm2 = UserFriend.objects.get(my_id=friend.id, friend_id=user)
        arrayMessages = MessagesFriend.objects.filter( Q(friend=idm1) | Q(friend=idm2))[-10:]
        return sorted(arrayMessages, key = MessagesFriend.get_datemsg)
    except:
        return None
@csrf_protect
def send_message(request):
    data = {}
    data['erro'] = []
    if request.method == 'POST':
        message = request.POST.get('message')
        try:
            friend_id = request.POST.get('friend_id')
            friend = AuthUser.objects.get(id=friend_id)
            idm1 = UserFriend.objects.get(my_id=request.user.id, friend_id=friend)
            print(idm1)
            msg = MessagesFriend(friend=idm1,message=message)
            msg.save()
        except: 
            data['erro'].append("Erro ao carregar mensagens! Tente novamente")
        return render(request, 'index.html')
    #redirect('messagesP')