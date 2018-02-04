from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from principal.views import RegistrarUsuarioView

urlpatterns = [
    path('', views.index, name="index"),
    #path('home', views.index, name="home"),
    path('turma/<int:id>', views.acessarTurma, name="acessarTurma"),
    path('turma/<int:idTurma>/aluno', views.acessarTurmaAluno, name="acessarTurmaAluno"),
    path('aluno/detalhes/<int:id>', views.acessarDetalhesAluno, name="detalhesAluno"),
    path('atividade/detalhes/<int:id>', views.getRespostasAtividade, name="getRespostas"),
    path('atividade/<int:id>', views.detalhesAtividade, name="detalhesAtividade"),
    path('atividade/lista', views.listarAtividades, name="listarAtividades"),
    path('login', auth_views.login, {'template_name':'login.html'}, name='login'),
    path('logout', auth_views.logout_then_login, {'login_url' : '/login'}, name="logout"),
    path('registrar', RegistrarUsuarioView.as_view(), name="registrar")
]