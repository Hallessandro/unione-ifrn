from django.db import models
import datetime
from datetime import date
from django.contrib.auth.models import User
from django.db.models import Count, Min, Sum, Avg
from quill.fields import RichTextField


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
    codigo = models.CharField(max_length=200, blank=False, null=False)    

class Atividade(models.Model):
    titulo = models.CharField(max_length=255, blank=False, null=False)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    data_entrega = models.DateField(default = datetime.date.today)
    turma = models.ForeignKey(Turma, related_name="turma", on_delete=models.CASCADE)
    url = models.CharField(max_length=1000, blank=False, null=False)
    individual = models.BooleanField(default=True)

    @property
    def comparaData(self):
        return self.data_entrega >= date.today()

class RespostaAtividade(models.Model):
    atividade = models.ForeignKey(Atividade, related_name="atividade", on_delete=models.CASCADE)
    aluno = models.ForeignKey(Usuario, related_name="aluno", on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=True, null=True)
    resposta = RichTextField(config='basic')

class Video(models.Model):
    titulo = models.CharField(max_length=1000, blank=False, null=False)
    embedCode = models.CharField(max_length=1000, blank=False, null=False)
    data_entrega = models.DateField(default = datetime.date.today)
    turma = models.ForeignKey(Turma, related_name="turma_acesso", on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=5, decimal_places=2)

    @property
    def comparaData(self):
        return self.data_entrega >= date.today()
class VideoAssistido(models.Model):
    aluno = models.ForeignKey(Usuario, related_name="aluno_video", on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name="video", on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=True, null=True)
    assistido = models.BooleanField(default=False)