from django.shortcuts import render
from principal.models import *
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    usuarioLogado = get_perfil_logado(request)
    turmas_aluno = Turma.objects.filter(alunos__id=usuarioLogado.id) 
    turmas_adm = Turma.objects.all().filter(administrador=usuarioLogado.id)
    return render(request, 'index.html', {'turmas_adm': turmas_adm,'usuarioLogado':usuarioLogado, 'turmas_aluno': turmas_aluno})

@login_required
def acessarTurma(request, id):
    usuarioLogado = get_perfil_logado(request)
    turma = Turma.objects.get(id=id)
    atividades = Atividade.objects.filter(turma=turma)
    return render(request, 'turmaDetalhes.html', {'turma': turma, 'atividades': atividades, 'usuarioLogado':usuarioLogado})

@login_required
def acessarTurmaAluno(request, idTurma):
    atividades = Atividade.objects.filter(turma__id=idTurma)
    respostas = RespostaAtividade.objects.filter(aluno__id=1000).filter(atividade__turma__id=idTurma)
    return render(request, 'turmasDetalheAluno.html', {'respostas': respostas, 'atividades' : atividades})

@login_required
def acessarDetalhesAluno(request, id):
    usuarioLogado = get_perfil_logado(request)
    aluno = Usuario.objects.get(id=usuarioLogado.id)
    return render(request, 'alunoDetalhes.html', {'aluno': aluno})   

@login_required
def getRespostasAtividade(request, id):
    respostas = RespostaAtividade.objects.filter(atividade=id)
    return render(request, 'respostasAtividade.html', {'respostas': respostas})

@login_required
def detalhesAtividade(request,id):
    atividade = Atividade.objects.get(id=id)
    return render(request, 'atividadeDetalhes.html', {'atividade': atividade})

@login_required
def get_perfil_logado(request):
    return request.user.usuario    