from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Tags, Raca, Pet
from django.contrib import messages
from django.contrib.messages import constants

@login_required(login_url='/auth/login/')
def novo_pet(request):
    if request.method == "GET":
        racas = Raca.objects.all()
        tags = Tags.objects.all()
        return render(request, "novo_pet.html", {'tags': tags, 'racas': racas})
    elif request.method == 'POST':
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get("descricao")
        estado = request.POST.get("estado")
        cidade = request.POST.get("cidade")
        telefone = request.POST.get("telefone")
        tags = request.POST.getlist("tags")
        raca = request.POST.get("raca")

        
        if len(nome.strip()) == 0 or len(descricao.strip()) == 0 or len(estado.strip()) == 0 or len(cidade.strip()) == 0 or len(telefone.strip()) == 0:
            messages.add_message(request, constants.WARNING, "preencha todos os campos")
            return redirect('/divulgar/novo_pet/')
        try:
            pet = Pet(
            usuario=request.user,
            foto=foto,
            nome=nome,
            descricao=descricao,
            estado=estado,
            cidade=cidade,
            telefone=telefone,
            raca_id=raca,
            )
            pet.save()
        except:
            messages.add_message(request, constants.ERROR, "erro do sistema")
            return redirect('/divulgar/novo_pet/')
        for tag_id in tags:
            tag = Tags.objects.get(id=tag_id)
            pet.tags.add(tag)
        pet.save()
        return redirect("/divulgar/seus_pets")
@login_required(login_url='/auth/login/')
def seus_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(usuario=request.user)
        return render(request, 'seus_pets.html', {'pets':pets})
@login_required(login_url='/auth/login/')
def remover_pet(request, id):
    pet = Pet.objects.get(id=id)
    if not pet.usuario == request.user:
        messages.add_message(request, constants.ERROR(" espertinho esse pet não é seu"))
        return redirect('/divulgar/seus_pets')
    pet.delete
    messages.add_message(request, constants.SUCCESS(" foi removido com sucesso"))
    return redirect("/divulgar/seus_pets/")