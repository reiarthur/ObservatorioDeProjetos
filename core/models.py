from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Categoria(models.Model):
    nome = models.CharField('Nome da categoria', max_length=255)

    def __str__(self):
        return self.nome

class Fase(models.Model):
    nome = models.CharField('Nome da fase', max_length=255)

    def __str__(self):
        return self.nome

class Projeto(models.Model):
    id = models.CharField('Id', max_length=255, primary_key=True)
    nome = models.CharField('Nome do projeto', max_length=255)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    convenio = models.CharField('Convênio', max_length=255, blank=True, null=True)
    contratada = models.CharField('Contratada', max_length=255, blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    prazo_dias = models.IntegerField(blank=True, null=True)
    data_conclusao = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nome

    def nome_truncado(self):
        return "%s%s" % (self.nome[:60], "...")

class Favorito(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + ' favoritou ' + self.projeto.nome

    def acao_str(self):
        return " favoritou o projeto " 

class Comentario(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    texto = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    #comentario_pai = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + ' comentou em ' + self.projeto.nome

    def acao_str(self):
        return " comentou sobre o projeto "