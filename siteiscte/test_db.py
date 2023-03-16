from votacao.models import Questao, Opcao

votos = 0
lista1 = Questao.objects.all()
for a in lista1:
    lista2 = a.opcao_set.all()
    opcao_preferida = ""
    n_votos = 0
    for b in lista2:
        votos += b.votos
        if b.votos > n_votos:
            opcao_preferida=b.opcao_texto
            n_votos = b.votos
    if n_votos <= 0:
        print(a,"/", opcao_preferida,"/", n_votos)
    else:
        print("Ninguem votou na questao:",a)
print("Numero total de Votos:", votos)
