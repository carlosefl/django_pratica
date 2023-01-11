from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
def cadastro(request):
    if request.user.is_authenticated:
        return render(request, '/divulgar/novo_pet')
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, "as senhas não são compativeis")
            return render(request, 'cadastro.html')
        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, "preencha todos os campos")
            return render(request, 'cadastro.html')
        #sucesso
        try:
            User.objects.create_user(username=nome,email=email, password= senha)
            messages.add_message(request, constants.SUCCESS, 'usuario criado com sucesso')
            return render(request, 'cadastro.html')
        #falha 
        except:
            return render(request, 'cadastro.html')
            messages.add_message(request, constants.ERROR, "erro interno do sistema")
        return HttpResponse('teste')
#view do login
def logar(request):
    if request.user.is_authenticated:
        return render(request, '/divulgar/novo_pet')
    if request.method == 'GET':
        return render(request, "login.html")
    elif request.method == "POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(username = nome, password = senha)
        if user is not None:
            login(request, user)
            return redirect ('/divulgar/novo_pet')
        else:
            messages.add_message(request, constants.WARNING, "verifique se os dados estão corretos")
            return render(request, "login.html")
#sair da conta
def sair(request):
    logout(request)
    return redirect('/auth/login')