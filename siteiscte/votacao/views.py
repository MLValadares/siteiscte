from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


from .models import Questao, Opcao

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
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {'questao': questao,'error_message': "Não escolheu uma opção",})
    else:
        opcao_seleccionada.votos += 1
        opcao_seleccionada.save()
    # Retorne sempre HttpResponseRedirect depois de
    # tratar os dados POST de um form
    # pois isso impede os dados de serem tratados
    # repetidamente se o utilizador
    # voltar para a página web anterior.
    return HttpResponseRedirect(reverse('votacao:resultados',args=(questao.id,)))

def criarquestao(request):
    return render(request, 'votacao/criarquestao.html')

def createquestion(request):
    if request.POST['questaotexto']=="":
        return render(request, 'votacao/criarquestao.html',{'error_message': "Não introduziu um texto", })
    q = Questao(questao_texto=request.POST['questaotexto'],pub_data=timezone.now())
    q.save()
    return render(request, 'votacao/criarquestao.html', {'error_message': "Nova pergunta criada", })

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


def logar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,
                            password=password)
        if user is not None:
            login(request, user)
            return render(request, 'votacao/index.html')
        else:
            return render(request, 'votacao/registar.html', {'error_message': "Erro ao criar a sua conta", })
    else:
        # se a invocação não veio do form, isto é, o 1º passo
        return render(request, 'votacao/logar.html')




def registar(request):
 if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    curso = request.POST['curso']
    u = User.objects.create_user(username, password)
    a = Aluno(user = u, email = email, curso = curso)
    return render(request, 'votacao/registar.html', {'error_message': "User registado com sucesso", })

 else:
    # se a invocação não veio do form, isto é, o 1º passo
    return render(request, 'votacao/registar.html')