from django import forms

class ComentarioForm(forms.Form):
    texto = forms.CharField()
    projeto = forms.CharField()

class FavoritoForm(forms.Form):
    projeto = forms.CharField()