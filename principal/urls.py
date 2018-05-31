from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from principal.views import RegistrarUsuarioView

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    #path('home', views.index, name="home"),

    path('turma/<int:id>', views.acessarTurma, name="acessarTurma"),
    path('turma/<int:idTurma>/aluno', views.acessarTurmaAluno, name="acessarTurmaAluno"),
    path('turma/buscar', views.consultaTurmaByCodigo, name="consultaTurmaByCodigo"),
    path('turma/cadastrar', views.cadastrarTurma, name='cadastrarTurma'),
    path('turma/<int:id>/entrar', views.entrarTurma, name='entrarTurma'),

    path('aluno/detalhes/<int:id>', views.acessarDetalhesAluno, name="detalhesAluno"),
    path('aluno/detalhes/<int:id>/turma/<int:idTurma>', views.acessarNotasAluno, name="notasAluno"),

    path('atividade/detalhes/<int:id>', views.getRespostasAtividade, name="getRespostas"),
    path('atividade/<int:id>', views.detalhesAtividade, name="detalhesAtividade"),
    path('atividade/lista', views.listarAtividades, name="listarAtividades"),
    path('atividade/resposta/<int:id>', views.verResposta, name="verResposta"),
    path('atividade/responder/<int:id>/usuario/<int:idAluno>', views.responderAtividade, name='responderAtividade'),
    path('atividade/cadastrar', views.cadastrarAtividade, name='cadastrarAtividade'),

    path('login', auth_views.login, {'template_name':'login.html'}, name='login'),
    path('logout', auth_views.logout_then_login, {'login_url' : '/login'}, name="logout"),
    path('registrar', RegistrarUsuarioView.as_view(), name="registrar"),

    path('alterarNota/<int:id>/pagina/<int:idPagina>', views.alterarNota, name='alterarNota'),

    path('video/lista', views.listarVideos, name='listaVideos'),
    path('video/cadastrar', views.cadastrarVideo, name='cadastrarVideo')
]