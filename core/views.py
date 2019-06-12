from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (LoginView, LogoutView)
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import (TemplateView, ListView, View)
from django.views.generic.detail import DetailView
from django.db.models import Count
from .models import Projeto, Comentario, Favorito
from .forms import ComentarioForm, FavoritoForm
from itertools import chain

# Create your views here.

class LandingView(TemplateView):
    template_name = 'core/login/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('core:board'))
        return super(LandingView, self).dispatch(request, *args, **kwargs)

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('core:landing_page')

"""class BoardView(TemplateView):
    template_name = 'core/board.html'

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)
        comentarios = Comentario.objects.all()
        favoritos = Favorito.objects.all()
        trend_projetos = Projeto.objects.annotate(num_comentarios=Count('comentario')).order_by('-num_comentarios')[:5]
        feed = sorted(chain(comentarios, favoritos), key=lambda instance: instance.created_at, reversed=Ture)
        context['feed'] = feed
        context['trend_projetos'] = trend_projetos
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('core:landing_page'))
        return super(BoardView, self).dispatch(request, *args, **kwargs)"""

class BoardView(ListView):
    template_name = 'core/board.html'
    model = Comentario

    def get_queryset(self):
        comentarios = Comentario.objects.all()
        favoritos = Favorito.objects.all()
        return sorted(chain(comentarios, favoritos), key=lambda instance: instance.created_at, reverse=True)

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)
        trend_projetos = Projeto.objects.annotate(num_comentarios=Count('comentario')).order_by('-num_comentarios')[:5]
        context['trend_projetos'] = trend_projetos
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('core:landing_page'))
        return super(BoardView, self).dispatch(request, *args, **kwargs)
    
class ProjetosListView(ListView):
    model = Projeto
    template_name = 'core/projetos.html'

class ProjetoDetailView(DetailView):
    model = Projeto
    template_name = 'core/projeto.html'

    def get_context_data(self, **kwargs):
        comentarios = Comentario.objects.filter(projeto=self.object)
        favorito = Favorito.objects.filter(projeto=self.object, user=self.request.user)
        context = super(ProjetoDetailView, self).get_context_data(**kwargs)
        context['comentarios'] = comentarios
        context['favorito'] = favorito.count() > 0
        return context


class ComentarView(View):
    def post(self, request, *args, **kwargs):
        form = ComentarioForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            projeto = Projeto.objects.get(id=form.cleaned_data['projeto'])
            comentario = Comentario(texto=form.cleaned_data['texto'], projeto=projeto, user=request.user)
            comentario.save()
            return redirect(reverse_lazy('core:projeto_detail', kwargs={ 'pk': projeto.id }))
        return redirect(reverse_lazy('core:landing_page'))
    
class FavoritarView(View):
    def post(self, request, *args, **kwargs):
        print("ENTROU")
        form = FavoritoForm(request.POST)
        print("pdifjsodf")
        if form.is_valid() and request.user.is_authenticated:
            print("sss")
            projeto = Projeto.objects.get(id=form.cleaned_data['projeto'])
            favorito = Favorito(projeto=projeto, user=request.user)
            favorito.save()
            return redirect(reverse_lazy('core:projeto_detail', kwargs={ 'pk': projeto.id }))
        return redirect(reverse_lazy('core:landing_page'))

class DesfavoritarView(View):
    def post(self, request, *args, **kwargs):
        form = FavoritoForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            projeto = Projeto.objects.get(id=form.cleaned_data['projeto'])
            favorito = Favorito.objects.filter(projeto=projeto, user=request.user)  
            favorito.delete()
            return redirect(reverse_lazy('core:projeto_detail', kwargs={ 'pk': projeto.id }))
        return redirect(reverse_lazy('core:landing_page'))