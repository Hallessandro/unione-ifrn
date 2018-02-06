from django.shortcuts import render, redirect
from principal.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from principal.forms import *

@login_required
def index(request):
    usuarioLogado = get_perfil_logado(request)
    turmas_aluno = Turma.objects.filter(alunos__id=usuarioLogado.id) 
    turmas_adm = Turma.objects.all().filter(administrador=usuarioLogado.id)
    return render(request, 'index.html', {'turmas_adm': turmas_adm,'usuarioLogado':usuarioLogado, 'turmas_aluno': turmas_aluno})

@login_required
def acessarTurma(request, id):
    ranking = []
    usuarioLogado = get_perfil_logado(request)
    turma = Turma.objects.get(id=id)
    atividades = Atividade.objects.filter(turma=turma)
    respostas = RespostaAtividade.objects.filter(atividade__turma__id = turma.id)
    for aluno in turma.alunos.all():   
        soma = 0
        for res in RespostaAtividade.objects.filter(aluno__id=aluno.id):
            soma += res.nota
        r = Ranking(aluno.id,aluno.nome, soma)
        ranking.append(r)
        rankingOrdenado = sorted(ranking, key=lambda Ranking:Ranking.resultado, reverse=True)
    return render(request, 'turmaDetalhes.html', {'turma': turma, 'atividades': atividades, 'usuarioLogado':usuarioLogado, 'ranking': rankingOrdenado})

@login_required
def listarAtividades(request):
    usuarioLogado = get_perfil_logado(request)
    atividadesProfessor = Atividade.objects.filter(turma__administrador__id=usuarioLogado.id)
    atividadesAluno = Atividade.objects.filter(turma__alunos__id=usuarioLogado.id)
    return render(request, 'listaAtividades.html', {'usuarioLogado': usuarioLogado, 'atividadesProfessor': atividadesProfessor, 'atividadesAluno': atividadesAluno})

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
    atividade = Atividade.objects.get(id=id)
    return render(request, 'respostasAtividade.html', {'respostas': respostas, 'atividade':atividade})

@login_required
def detalhesAtividade(request,id):
    atividade = Atividade.objects.get(id=id)
    return render(request, 'atividadeDetalhes.html', {'atividade': atividade})

@login_required
def get_perfil_logado(request):
    return request.user.usuario    

class RegistrarUsuarioView(View):
    template = 'cadastroUsuario.html'
    def get(self, request):
        return render(request, self.template)
    def post(self,request):
        #preenche o from
        form = RegistrarUsuarioForm(request.POST)

        #verifica se eh valido
        if form.is_valid():

            dados_form = form.data

            #cria o usuario
            usuario = User.objects.create_user(dados_form['nome'], dados_form['email'], dados_form['senha'])            

            #cria o perfil
            perfil = Usuario(nome=dados_form['nome'],
                            matricula=dados_form['matricula'],
                            usuario=usuario)

            #grava no banco
            perfil.save()

            #redireciona para index
            return redirect('login')

        #so chega aqui se nao for valido
        #vamos devolver o form para mostrar o formulario preenchido 
        return render(request, self.template_name, {'form' : form})


class Ranking(object):
    idAluno = 0
    nomeAluno = ''
    resultado = 0.0

    def __init__(self, idAluno, nome, resultado):
        self.idAluno = idAluno
        self.nomeAluno = nome
        self.resultado = resultado