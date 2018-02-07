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
            #soma = soma + res.nota
            pass
        r = Ranking(aluno.id,aluno.nome, soma, turma.id)
        ranking.append(r)
        rankingOrdenado = sorted(ranking, key=lambda Ranking:Ranking.resultado, reverse=True)
    return render(request, 'turmaDetalhes.html', {'turma': turma, 'atividades': atividades, 'usuarioLogado':usuarioLogado, 'ranking': rankingOrdenado})

@login_required
def verResposta(request, id):
    resposta = RespostaAtividade.objects.get(id=id)
    usuarioLogado = get_perfil_logado(request)
    return render(request, 'verResposta.html', {'resposta': resposta, 'usuarioLogado':usuarioLogado})

@login_required
def listarAtividades(request):
    usuarioLogado = get_perfil_logado(request)
    atividadesProfessor = Atividade.objects.filter(turma__administrador__id=usuarioLogado.id)
    atividadesAluno = Atividade.objects.filter(turma__alunos__id=usuarioLogado.id)
    return render(request, 'listaAtividades.html', {'usuarioLogado': usuarioLogado, 'atividadesProfessor': atividadesProfessor, 'atividadesAluno': atividadesAluno})

@login_required
def alterarNota(request, id, idPagina):    
    novaNota = request.POST.get('nota')
    resposta = RespostaAtividade.objects.get(id=id)
    resposta.nota = novaNota
    resposta.save()
    usuarioLogado = get_perfil_logado
    if(idPagina == 1):
        return render(request, 'verResposta.html', {'resposta': resposta, 'usuarioLogado':usuarioLogado})
    else:
        respostas = RespostaAtividade.objects.filter(atividade__id=resposta.atividade.id)
        atividade = Atividade.objects.get(id=resposta.atividade.id)
        return render(request, 'respostasAtividade.html', {'respostas': respostas, 'atividade':atividade, 'usuarioLogado':usuarioLogado})

@login_required
def responderAtividade(request, id, idAluno):
    usuarioLogado = get_perfil_logado(request)
    if(request.method == 'GET'):
        return render(request, 'respostaAtividadeForm.html', {'usuarioLogado': usuarioLogado})
    elif(request.method == "POST"):
        resposta = request.POST.get('froala-editor')
        atividade = Atividade.objects.get(id=id)
        aluno = Usuario.objects.get(id=idAluno)
        r = RespostaAtividade()
        r.aluno = aluno
        r.atividade = atividade
        r.nota = 0
        r.resposta = resposta
        r.save()
        return render(request, 'minhasRespostas.html', {'usuarioLogado': usuarioLogado})

@login_required
def acessarTurmaAluno(request, idTurma):
    usuarioLogado = get_perfil_logado(request)
    atividades = Atividade.objects.filter(turma__id=idTurma)
    respostas = RespostaAtividade.objects.filter(aluno__id=1000).filter(atividade__turma__id=idTurma)
    return render(request, 'turmasDetalheAluno.html', {'respostas': respostas, 'atividades' : atividades, 'usuarioLogado': usuarioLogado})

@login_required
def acessarDetalhesAluno(request, id):
    usuarioLogado = get_perfil_logado(request)
    aluno = Usuario.objects.get(id=usuarioLogado.id)
    return render(request, 'alunoDetalhes.html', {'aluno': aluno, 'usuarioLogado': usuarioLogado})   

@login_required
def acessarNotasAluno(request, id, idTurma):
    usuarioLogado = get_perfil_logado(request)
    atividades = Atividade.objects.filter(turma__id=idTurma)
    respostas = RespostaAtividade.objects.filter(atividade__turma__id=idTurma).filter(aluno__id=id)
    return render(request, 'notasAluno.html', {'respostas':respostas, 'atividades':atividades, 'usuarioLogado':usuarioLogado})

@login_required
def getRespostasAtividade(request, id):
    usuarioLogado = get_perfil_logado(request)
    respostas = RespostaAtividade.objects.filter(atividade=id)
    atividade = Atividade.objects.get(id=id)
    return render(request, 'respostasAtividade.html', {'respostas': respostas, 'atividade':atividade, 'usuarioLogado':usuarioLogado})

@login_required
def detalhesAtividade(request,id):
    usuarioLogado = get_perfil_logado(request)
    atividade = Atividade.objects.get(id=id)
    return render(request, 'atividadeDetalhes.html', {'atividade': atividade, 'usuarioLogado':usuarioLogado})

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
    idTurma = 0

    def __init__(self, idAluno, nome, resultado, idTurma):
        self.idAluno = idAluno
        self.nomeAluno = nome
        self.resultado = resultado
        self.idTurma = idTurma