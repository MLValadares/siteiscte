from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Questao, Opcao, Aluno

# Feito por Grupo LEI-3
limite_votos=13

def index(request):
    latest_question_list =Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html',context)


def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html',{'questao': questao})


def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


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
    if (request.POST['action']=="Remover Opção selecionada"):
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

def createquestion(request):
    if request.POST['questaotexto']=="":
        return render(request, 'votacao/criarquestao.html',{'error_message': "Não introduziu um texto", })
    q = Questao(questao_texto=request.POST['questaotexto'],pub_data=timezone.now())
    q.save()
    return render(request, 'votacao/criarquestao.html', {'error_message': "Nova pergunta criada"})

def remove_question(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    questao.delete()
    # falta por messagem de erro a dizer com sucesso
    # {'error_message': "Pergunta apagada com sucesso"}
    return HttpResponseRedirect(reverse('votacao:index'))

def criaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/criaropcao.html', {'questao': questao})

def createoption(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    if request.POST['opcaotexto'] == "":
        return render(request, 'votacao/criaropcao.html', {'questao': questao,'error_message': "Não introduziu um texto", })
    o = Opcao(opcao_texto=request.POST['opcaotexto'],votos=0,questao=questao)
    o.save()
    return render(request, 'votacao/criaropcao.html', {'questao': questao, 'error_message': "Nova opção criada"})
'''
 def remove_option(request, opcao_id):
    o = get_object_or_404(Opcao, pk=opcao_id)
    if request.POST['opcaotexto']=="":
        return render(request, 'votacao/detalhe.html', {'error_message': "Não introduziu um texto", })
    else:
        o.delete()
        return HttpResponseRedirect(reverse('votacao:detalhe'))'''

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

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:index'))

def user_view(request):
    return render(request, 'votacao/user_view.html')
