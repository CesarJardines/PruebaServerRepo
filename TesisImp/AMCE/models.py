from django.db import models
#se importan el modelo Usuario que viene por defecto en Django
from django.contrib.auth.models import User
#se importa la zona horaria 
from django.utils import timezone 

def get_name(self):
    return '{} {}'.format(self.last_name, self.first_name)

User.add_to_class("__str__", get_name)

class UserType(models.Model):
	userType = models.OneToOneField(User, on_delete=models.CASCADE)
	flag = models.IntegerField(choices=((1, 'Student'),(2, 'Teacher')), default=1)

class Grupos(models.Model):
	codigo = models.CharField(max_length=10, primary_key=True)
	grupo = models.CharField(max_length=100)
	materia = models.CharField(max_length=100,null=True,blank=True,default=None)
	institucion = models.CharField(max_length=100,null=True,blank=True,default=None)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f'Tema: {self.grupo} código:{self.codigo}'		

class Inscribir(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	codigo_materia = models.ForeignKey(Grupos, on_delete=models.CASCADE)

class Temas(models.Model):
	id_tema = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=100)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Equipos(models.Model):
	id_equipo = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=100)
	codigo_materia = models.ForeignKey(Grupos, on_delete=models.CASCADE)

class Asignar(models.Model):
	id_equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE)
	id_tema = models.ForeignKey(Temas, on_delete=models.CASCADE)

class Pertenecer(models.Model):
	id_equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)

#Esto es lo que agregué

class Actividad(models.Model):
	id_actividad = models.AutoField(primary_key=True)
	contenido = models.TextField()
	hora = models.DateTimeField(default = timezone.now)
	pasoMG = models.FloatField(null=True,blank=True,default=None)
	id_tema = models.ForeignKey(Temas, on_delete=models.CASCADE, null=True,blank=True,default=None)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True,default=None)
	voto = models.IntegerField(default=0)

class Hace(models.Model):
	id_equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE)
	id_actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
	id_tema = models.ForeignKey(Temas, on_delete=models.CASCADE, null=True,blank=True,default=None)
	comentario = models.TextField(default='')

class Post(models.Model):
	'''
	Atributos de Post
	'''
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
	timestamp = models.DateTimeField(default = timezone.now)
	content = models.TextField()
	#codigo_materia = models.ForeignKey(Clases, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-timestamp']
