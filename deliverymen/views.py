# seu_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DeliveryMan
from company.forms import DeliveryManForm

# View para LISTAR entregadores e CRIAR um novo
@login_required(login_url="login")
def entregadores(request, status='todos'):
    # --- Lógica para CRIAR (POST) ---
    if request.method == "POST":
        form = DeliveryManForm(request.POST, request.FILES)
        if form.is_valid():
            entregador = form.save(commit=False)
            entregador.user = request.user
            entregador.save()
            messages.success(request, 'Entregador cadastrado com sucesso!')
            return redirect('entregador_list') # Redireciona para a lista principal
        else:
            messages.error(request, 'Houve um erro no formulário. Corrija os campos destacados.')
    else:
        form = DeliveryManForm() # Formulário vazio para a requisição GET

    # --- Lógica para LISTAR (GET) ---
    if status == 'ativo':
        entregadores_cadastrados = DeliveryMan.objects.filter(user=request.user, is_active=True)
    elif status == 'inativo':
        entregadores_cadastrados = DeliveryMan.objects.filter(user=request.user, is_active=False)
    else: # status == 'todos'
        entregadores_cadastrados = DeliveryMan.objects.filter(user=request.user)

    context = {
        'form': form,
        'entregadores': entregadores_cadastrados,
        'status_atual': status, # Para saber qual filtro está ativo no template
    }
    return render(request, "entregadores_teste.html", context)

# View para VISUALIZAR detalhes de UM entregador
@login_required(login_url="login")
def entregadores_detalhes(request, pk):
    # Busca o entregador pelo ID (pk) E garante que ele pertence ao usuário logado
    entregador = get_object_or_404(DeliveryMan, pk=pk, user=request.user)
    context = {
        'entregador': entregador
    }
    return render(request, 'entregadores/entregador_detail.html', context)

# View para EDITAR UM entregador
@login_required(login_url="login")
def entregador_update(request, pk):
    entregador = get_object_or_404(DeliveryMan, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Passa a 'instance' para o formulário saber qual objeto deve ser atualizado
        form = DeliveryManForm(request.POST, request.FILES, instance=entregador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do entregador atualizados com sucesso!')
            return redirect('entregador_list')
    else:
        # Se for GET, cria o formulário já preenchido com os dados do entregador
        form = DeliveryManForm(instance=entregador)

    context = {
        'form': form,
        'entregador': entregador
    }
    return render(request, 'entregadores/entregador_form.html', context)

# View para REMOVER UM entregador
@login_required(login_url="login")
def entregador_delete(request, pk):
    entregador = get_object_or_404(DeliveryMan, pk=pk, user=request.user)
    
    if request.method == 'POST':
        entregador.delete()
        messages.success(request, 'Entregador removido com sucesso!')
        return redirect('entregador_list')
        
    context = {
        'entregador': entregador
    }
    return render(request, 'entregadores/entregador_confirm_delete.html', context)