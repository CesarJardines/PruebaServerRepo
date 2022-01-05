from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
#Heredo del userCreationForm que viene en django
class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', "first_name", "last_name", "email", "password1", "password2"]

class CodeForm(forms.ModelForm):
	code = forms.CharField(label='Ingresa el código de la clase', widget=forms.Textarea(attrs={'rows':2, 'placeholder': 'Ingresa tu respuesta'}))

class FormActividadPI(forms.Form):
	contenido = forms.CharField(label='', max_length = 500, widget=forms.Textarea(attrs={'rows':2, 'placeholder': 'Ingresa tu pregunta inicial'}))


class PostPreguntaInicial(forms.ModelForm):
	#Aqui se obtiene el campo de contenido de nuestro modelo Forms para Post
	content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':2, 'placeholder': 'Ingresa tu pregunta inicial'}))

	class Meta:
		model = Post
		fields = ['content']

""" FORMS PROFESOR """

class FormCrearGrupo(forms.Form):
	nombre = forms.CharField(label='Nombre del grupo', max_length = 350)
	materia = forms.CharField(label='Materia', max_length =110)
	institucion = forms.CharField(label='Institución', max_length = 350) 

class FormCrearTema(forms.Form):
	nombre = forms.CharField(label='Nombre del tema', max_length = 100)

class FormCrearEquipo(forms.Form):
	nombre = forms.CharField(label='Nombre del equipo',max_length=100)
	integrantes = forms.MultipleChoiceField(choices=User.objects.all().values_list('id', 'last_name'),widget=forms.SelectMultiple)
	def __init__(self,*args,**kwargs):
		codigo = ''
		if 'codigo' in kwargs.keys():
			codigo = kwargs.pop('codigo')
		super().__init__(*args, **kwargs)
		if codigo != '':
			print(codigo)
			inscritos = Inscribir.objects.filter(codigo_materia=codigo).values_list('user_id', flat=True)
			usuarios = User.objects.filter(id__in=inscritos).order_by('last_name','first_name').values_list('id','last_name','first_name')
			estudiantes = []
			for i in usuarios:
				estudiantes.append((i[0],i[1] + " " + i[2]))
			print(usuarios)
			self.fields['integrantes'].choices = estudiantes

class AsignarTemaGrupo(forms.Form):
	tema = forms.ChoiceField(label='Tema',choices=Temas.objects.all().values_list('id_tema','nombre'))
	equipos = forms.MultipleChoiceField(choices=Equipos.objects.all().values_list('id_equipo', 'nombre'),widget=forms.SelectMultiple)
	def __init__(self,*args,**kwargs):
		codigo = ''
		if 'codigo' in kwargs.keys():
			codigo = kwargs.pop('codigo')
		super().__init__(*args, **kwargs)
		if codigo != '':
			user_id = Grupos.objects.get(codigo=codigo).user_id
			temas = Temas.objects.filter(user_id=user_id).values_list('id_tema','nombre')
			equipos = Equipos.objects.filter(codigo_materia=codigo).values_list('id_equipo', 'nombre')
			self.fields['tema'].choices = temas
			self.fields['equipos'].choices = equipos
