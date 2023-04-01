from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Questao, Opcao, Aluno

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Feito por Grupo LEI-3
limite_votos=13

from django.contrib.auth.decorators import login_required
import os

def index(request):
    latest_question_list =Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html',context)


def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html',{'questao': questao})

#autheticado
def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})

@login_required(login_url='/votacao/logar')
def voto(request, questao_id):
    if (request.POST['action']=="Voto"):
        questao = get_object_or_404(Questao, pk=questao_id)
        try:
            opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
        except (KeyError, Opcao.DoesNotExist):
            # Apresenta de novo o form para votar
            return render(request, 'votacao/detalhe.html', {'questao': questao,'error_message': "Não escolheu uma opção",})
        else:
            if not request.user.is_superuser:
                if request.user.aluno.votos >= limite_votos:
                    return render(request, 'votacao/detalhe.html', {'questao': questao,'error_message': "Limite de votos atingido"})
                else:
                    aluno = get_object_or_404(Aluno, pk=request.user.aluno.pk)
                    aluno.votos+=1
                    aluno.save()
            opcao_seleccionada.votos += 1
            opcao_seleccionada.save()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
        return HttpResponseRedirect(reverse('votacao:resultados',args=(questao.id,)))
    # apenas admin
    if (request.POST['action']=="Remover Opção selecionada"):
        if not request.user.is_superuser:
            return Http404("O utilizador não tem permissões")
        questao = get_object_or_404(Questao, pk=questao_id)
        try:
            o = questao.opcao_set.get(pk=request.POST['opcao'])
        except (KeyError, Opcao.DoesNotExist):
            # Apresenta de novo o form para votar
            return render(request, 'votacao/detalhe.html', {'questao': questao,'error_message': "Não escolheu uma opção",})
        o.delete()
        return HttpResponseRedirect(reverse('votacao:detalhe',args=(questao.id,)))

def criarquestao(request):
    return render(request, 'votacao/criarquestao.html')

#apenas admin
def createquestion(request):
    if not request.user.is_authenticated:
        return Http404("O utilizador não está logado")
    else:
        if not request.user.is_superuser:
            return Http404("O utilizador não tem permissões")
    if request.POST['questaotexto']=="":
        return render(request, 'votacao/criarquestao.html',{'error_message': "Não introduziu um texto", })
    q = Questao(questao_texto=request.POST['questaotexto'],pub_data=timezone.now())
    q.save()
    return render(request, 'votacao/criarquestao.html', {'error_message': "Nova pergunta criada"})

#apenas admin
def remove_question(request, questao_id):
    if not request.user.is_authenticated:
        return Http404("O utilizador não está logado")
    else:
        if not request.user.is_superuser:
            return Http404("O utilizador não tem permissões")
    questao = get_object_or_404(Questao, pk=questao_id)
    questao.delete()
    return HttpResponseRedirect(reverse('votacao:index'))

def criaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/criaropcao.html', {'questao': questao})

#apenas admin
def createoption(request, questao_id):
    if not request.user.is_authenticated:
        return Http404("O utilizador não está logado")
    else:
        if not request.user.is_superuser:
            return Http404("O utilizador não tem permissões")
    questao = get_object_or_404(Questao, pk=questao_id)
    if request.POST['opcaotexto'] == "":
        return render(request, 'votacao/criaropcao.html', {'questao': questao,'error_message': "Não introduziu um texto", })
    o = Opcao(opcao_texto=request.POST['opcaotexto'],votos=0,questao=questao)
    o.save()
    return render(request, 'votacao/criaropcao.html', {'questao': questao, 'error_message': "Nova opção criada"})

def logar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,
                            password=password)
        if user is not None:
            login(request, user)
            return render(request, 'votacao/logar.html', {'error_message': "Logado com sucesso", })
        else:
            return render(request, 'votacao/logar.html', {'error_message': "Erro ao logar na sua conta", })
    else:
        # se a invocação não veio do form, isto é, o 1º passo
        return render(request, 'votacao/logar.html')

# não estar registado
def registar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        curso = request.POST['curso']
        u = User.objects.create_user(username,email, password)
        a = Aluno(user = u, curso = curso)
        a.save()
        if a is not None:
            return render(request, 'votacao/registar.html', {'error_message': "User registado com sucesso", })
        else:
            return render(request, 'votacao/registar.html', {'error_message': "User não foi registado com sucesso por favor tente novamente", })

    else:
        # se a invocação não veio do form, isto é, o 1º passo
        return render(request, 'votacao/registar.html')

#autheticado
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:index'))

#autheticado
def user_view(request):
    return render(request, 'votacao/user_view.html')

#autheticado
# exister maneira de guardar file em BD (forms.FileField), no entanto, decidimos usar como aparece no pdf de ficheiros estaticos
def fazer_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        aluno = get_object_or_404(Aluno, pk=request.user.aluno.pk)
        k = "foto_perfil_"+str(aluno.pk)+".png"
        if fs.exists(k):
            os.remove(fs.path(k))
        filename = fs.save(k, myfile)
        k="/static/media/foto_perfil_"+str(aluno.pk)+".png"
        aluno.foto_perfil= k
        aluno.save()
        uploaded_file_url = fs.url(filename)
        return render(request, 'votacao/fazer_upload.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'votacao/fazer_upload.html')
