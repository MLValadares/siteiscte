from django.urls import include, path
from . import views
# (. significa que importa views da mesma directoria)
app_name = 'votacao'
urlpatterns = [
# ex: votacao/
path("", views.index, name='index'),
# ex: votacao/1
path('<int:questao_id>', views.detalhe, name='detalhe'),
# ex: votacao/3/resultados
path('<int:questao_id>/resultados', views.resultados, name='resultados'),
# ex: votacao/5/voto
path('<int:questao_id>/voto', views.voto, name='voto'),
# votacao/criarquestao
path('criarvotacao', views.criarquestao, name='criarquestao'),
# votacao/createquestion
path('createquestion', views.createquestion, name='createquestion'),
# votacao/1/criaropcao
path('<int:questao_id>/criaropcao', views.criaropcao, name='criaropcao'),
# votacao/1/createoption
path('<int:questao_id>/createoption', views.createoption, name='createoption'),
# votacao/logar
path('logar', views.logar, name='logar'),
# votacao/registar
path('registar', views.registar, name='registar'),
# votacao/logout_view
path('logout_view', views.logout_view, name="logout_view"),
# votacao/user_view
path('user_view', views.user_view, name="user_view")
]