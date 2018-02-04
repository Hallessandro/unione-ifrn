from django.db import models
import datetime
from datetime import date
from django.contrib.auth.models import User
# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=255, blank=False, null=False)
    matricula = models.CharField(max_length=255, blank=False, null=False)
    usuario = models.OneToOneField(User, related_name="usuario",  on_delete=models.CASCADE)

    @property
    def email(self):
        return self.usuario.email

class Turma(models.Model):
    titulo = models.CharField(max_length=255, blank=False, null=False)
    administrador = models.ForeignKey(Usuario, related_name="adm_turma", on_delete=models.CASCADE)
    alunos = models.ManyToManyField(Usuario)
    descricao = models.CharField(max_length=1000, blank=True, null=True)

class Atividade(models.Model):
    titulo = models.CharField(max_length=255, blank=False, null=False)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    data_entrega = models.DateField(default = datetime.date.today)
    turma = models.ForeignKey(Turma, related_name="turma", on_delete=models.CASCADE)
    url = models.CharField(max_length=1000, blank=False, null=False)

    @property
    def comparaData(self):
        return self.data_entrega > date.today()

class RespostaAtividade(models.Model):
    atividade = models.ForeignKey(Atividade, related_name="atividade", on_delete=models.CASCADE)
    aluno = models.ForeignKey(Usuario, related_name="aluno", on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    resposta = models.CharField(max_length=2000, blank=False, null=False)

