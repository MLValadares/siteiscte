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
from django.urls import reverse_lazy
# Feito por Grupo LEI-3
limite_votos=13

from django.contrib.auth.decorators import login_required, user_passes_test
import os

def index(request):
    latest_question_list =Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html',context)


def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html',{'questao': questao})

#autheticado
@login_required(login_url=reverse_lazy('votacao:logar'))
def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})

@login_required(login_url=reverse_lazy('votacao:logar'))
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
    # esta verificão de super_user tem de ser feita dentro da função, porque a view é usada quer para votar, quer para apagar opções
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
@user_passes_test(lambda u: u.is_superuser,login_url=reverse_lazy('votacao:logar'))
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
@user_passes_test(lambda u: u.is_superuser,login_url=reverse_lazy('votacao:logar'))
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
@user_passes_test(lambda u: u.is_superuser,login_url=reverse_lazy('votacao:logar'))
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
@login_required(login_url='/votacao/logar')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:index'))

#autheticado
@login_required(login_url='/votacao/logar')
def user_view(request):
    return render(request, 'votacao/user_view.html')

#autheticado
# exister maneira de guardar file em BD (forms.FileField), no entanto, decidimos usar como aparece no pdf de ficheiros estaticos
@login_required(login_url='/votacao/logar')
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

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import * #(2)
from .models import Questao, Opcao
@api_view(['GET', 'POST']) #(3)
def questoes_lista(request):
    if request.method == 'GET': #(4)
        questoes = Questao.objects.all()
        serializerQ = QuestaoSerializer(questoes, context={'request':request}, many=True)
        return Response(serializerQ.data)
    elif request.method == 'POST': #(4)
        serializer = QuestaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE']) #(3) e (5)
def questoes_edita(request, pk):
    try:
        questao = Questao.objects.get(pk=pk)
    except Questao.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = QuestaoSerializer(questao,data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        questao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def opcoes_lista(request):
    if request.method == 'GET':
        opcoes = Opcao.objects.all()
        serializerO = OpcaoSerializer(opcoes, context={'request':request}, many=True)
        return Response(serializerO.data)
    elif request.method == 'POST':
        serializer = OpcaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def opcoes_edita(request, pk):
    try:
        opcao = Opcao.objects.get(pk=pk)
    except Opcao.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = OpcaoSerializer(opcao,data=request.data,context={'request': request})
        if serializer.is_valid():
            opcao.votos = opcao.votos + 1
            opcao.save()
            #serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        opcao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)