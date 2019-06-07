
from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [

    path('', LandingView.as_view(), name='landing_page'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('board/', BoardView.as_view(), name='board'),
    path('projetos/', ProjetosListView.as_view(), name='projetos'),
    path('projeto/<str:pk>/', ProjetoDetailView.as_view(), name='projeto_detail'),
    path('projeto/<str:pk>/comentar', ComentarView.as_view(), name='comentar'),
    path('projeto/<str:pk>/favoritar', FavoritarView.as_view(), name='favoritar'),
    path('projeto/<str:pk>/desfavoritar', DesfavoritarView.as_view(), name='desfavoritar')

]