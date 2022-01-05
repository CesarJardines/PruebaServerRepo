from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse
#se importa para aumentar el contador de votos en feed
from django.db.models import F
import random
import string

"""
	VISTAS/FUNCIONES COMPARTIDAS
"""

def index(request):
	return render(request, "index.html")

def registro(request):
	data = {
		'form': CustomUserCreationForm()
	}
	if request.method == "POST":
		formulario = CustomUserCreationForm(data=request.POST)
		if formulario.is_valid():
			usuario = formulario.save()
			usuario.save()
			user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])

			login(request,user)
			messages.success(request, "Registro exitoso, inicia sesión")
			return redirect(to="AMCE:bienvenida")
		data["form"] = formulario
	return render(request,'registration/registro.html',data)

def bienvenida(request):
	return render(request,"registration/bienvenida.html")

"""
	VISTAS/FUNCIONES DE ESTUDIANTE
"""

def alumno(request):
	current_user = get_object_or_404(User, pk=request.user.pk)
	usuarioTipo = UserType(userType=current_user,flag=1)
	usuarioTipo.save()
	return render(request,"estudiante/SelEquipo.html")

def AlumnoUnirseGrupo(request):
	inscribir = Inscribir()
	current_user = get_object_or_404(User, pk=request.user.pk)
	a = request.POST
	args = {'form': a}
	if request.method == 'POST':
		print(a)
		codigo_ingresado = request.POST.get("new")
		repetido = Inscribir.objects.filter(user_id=current_user,codigo_materia=codigo_ingresado)
		try:
			# Your code goes here
			inscribir.codigo_materia = Grupos.objects.get(codigo = request.POST.get("new"))
			if repetido.exists():
				print("Ya estas inscrito en este grupo")
				messages.add_message(request, messages.INFO, 'Ya estas inscrito')
				return redirect(to="AMCE:MG1")
			else:
				codigo_clase = Inscribir(user_id=current_user,codigo_materia=inscribir.codigo_materia)
				#inscribir.save()
				messages.add_message(request, messages.INFO, 'Grupo añadido')
				codigo_clase.save()
				return redirect(to="AMCE:MG1")
		except Grupos.DoesNotExist:
   			# Handle error here
   			print("ingresa un código valido")
   			messages.error(request, 'Ingresa un código valido')
   			return redirect(to="AMCE:MG1")
	return render(request,"estudiante/crear.html",args)

@login_required
def MG1(request):
	#Muestro las Grupos asignadas al ID del usuario actual en la página html
	code = Inscribir.objects.filter(user_id_id=request.user.pk)
	current_user = get_object_or_404(User, pk=request.user.pk)
	usuarioTipo = UserType.objects.filter(userType=current_user,flag=2)

	if(usuarioTipo):
		print("Eres maestro")
		return redirect(to="AMCE:ProfMisGrupos")
	else:
		usuarioTipoAlumno = UserType.objects.filter(userType=current_user,flag=1)
		if(usuarioTipoAlumno.exists()):
			print("Eres estudiante")
		else:
			usuarioTipo2 = UserType(userType=current_user,flag=1)
			usuarioTipo2.save()
	args = {'code':code}
	return render(request,"estudiante/SelEquipo.html",args)

def PaginaActividadAlumno(request, tema, codigo):
	
	current_user = get_object_or_404(User, pk=request.user.pk)
	'''
	pertenece = Pertenecer.objects.filter(user_id=current_user)
	equipo = Equipos.objects.get(codigo_materia=codigo) 
	asignar = Asignar.objects.filter(id_equipo=equipo.id_equipo)
	'''
	ids_equipos_relacionados_usuario = Pertenecer.objects.filter(user_id=current_user).values_list('id_equipo', flat=True)
	ids_equipos_relacionados_grupo = Equipos.objects.filter(codigo_materia=codigo, id_equipo__in=ids_equipos_relacionados_usuario)
	ids_temas = Asignar.objects.filter(id_equipo__in=ids_equipos_relacionados_grupo).values_list('id_tema', flat=True)
	temas = Temas.objects.filter(id_tema__in=ids_temas)

	return render(request, 'estudiante/Actividad.html',{'tema':tema, 'codigo':codigo, 'ids_temas':ids_temas.first()})

def PaginaAlumnoTema(request, codigo):
	
	current_user = get_object_or_404(User, pk=request.user.pk)
	grupo = Grupos.objects.filter(codigo=codigo)
	#Saco los usuarios relacionados a un equipo
	ids_equipos_relacionados_usuario = Pertenecer.objects.filter(user_id=current_user).values_list('id_equipo', flat=True)
	#saco los equipos relacionados a una materia (código)
	ids_equipos_relacionados_grupo = Equipos.objects.filter(codigo_materia=codigo, id_equipo__in=ids_equipos_relacionados_usuario)
	print(ids_equipos_relacionados_grupo)
	#saco los temas relacionados a los equipos del grupo de la materia
	ids_temas = Asignar.objects.filter(id_equipo__in=ids_equipos_relacionados_grupo).values_list('id_tema', flat=True)
	print(ids_temas)
	temas = Temas.objects.filter(id_tema__in=ids_temas)


	return render(request, 'estudiante/PaginaAlumnoTema.html', {'codigo':codigo ,'grupo':grupo.first(), 'temas':temas})

def postPreguntaInicial(request, tema ,codigo):
	current_user = get_object_or_404(User, pk=request.user.pk)
	tema_actual = Temas.objects.filter(nombre = tema).values_list('id_tema', flat=True)
	tema_actual_intancia = Temas.objects.get(id_tema__in=tema_actual)
	ids_equipos_relacionados_usuario = Pertenecer.objects.filter(user_id=current_user).values_list('id_equipo', flat=True)
	ids_equipos_relacionados_grupo = Equipos.objects.get(codigo_materia=codigo, id_equipo__in=ids_equipos_relacionados_usuario)
	print(ids_equipos_relacionados_grupo.id_equipo)
	if request.method == 'POST':
		form = FormActividadPI(request.POST)
		if form.is_valid():
			nueva_actividad = Actividad(contenido= form.cleaned_data['contenido'],
			 							pasoMG = 1.1,
			 							id_tema_id=Temas.objects.get(nombre=tema).id_tema,
			 							user=current_user)
			messages.add_message(request, messages.INFO, 'Respuesta capturada')
			nueva_actividad.save()
			nueva_hace = Hace(id_equipo_id= ids_equipos_relacionados_grupo.id_equipo,
								id_actividad_id=nueva_actividad.id_actividad,
								id_tema_id=Temas.objects.get(nombre=tema).id_tema)
			nueva_hace.save()
			return redirect('AMCE:feed' , codigo=codigo, tema=tema)
	else:
		form = FormActividadPI()
	return render(request, 'estudiante/PreguntaInicial.html', {'form': form, 'codigo':codigo, 'tema':tema})

def feed(request, tema, codigo):
	current_user = get_object_or_404(User, pk=request.user.pk)
	ids_equipos_relacionados_usuario = Pertenecer.objects.filter(user_id=current_user).values_list('id_equipo', flat=True)
	ids_equipos_relacionados_grupo = Equipos.objects.filter(codigo_materia=codigo, id_equipo__in=ids_equipos_relacionados_usuario)
	#Se obtiene el id del tema actual 
	prueba2 = Temas.objects.filter(nombre=tema).values_list('id_tema', flat=True)
	ids_equipo_relacionado_tema = Temas.objects.get(id_tema__in=prueba2)
	#Se obtiene el equipo relacionado al usuario actual con el tema actual, esto para sacar el id de equipo
	id_equipo_relacionado_tema_count = Asignar.objects.get(id_equipo__in=ids_equipos_relacionados_usuario, id_tema=ids_equipo_relacionado_tema)
	#Se muestra equipo en tema actual
	muestra_equipo = Pertenecer.objects.filter(id_equipo_id=id_equipo_relacionado_tema_count.id_equipo).count()
	print(muestra_equipo)

	hace_equipo = Hace.objects.filter(id_equipo__in=ids_equipos_relacionados_grupo, id_tema=ids_equipo_relacionado_tema)
	print(hace_equipo.count())

	if muestra_equipo == hace_equipo.count():
		return redirect('AMCE:feedPIHecha' , codigo=codigo, tema=tema)
	else:
		print("No todos han hecho esta actividad")
	return render(request, 'estudiante/feed.html', {'hace_equipo':hace_equipo, 'codigo':codigo, 'tema':tema})

def feedPIHecha(request, tema, codigo):
	current_user = get_object_or_404(User, pk=request.user.pk)
	ids_equipos_relacionados_usuario = Pertenecer.objects.filter(user_id=current_user).values_list('id_equipo', flat=True)
	ids_equipos_relacionados_grupo = Equipos.objects.filter(codigo_materia=codigo, id_equipo__in=ids_equipos_relacionados_usuario)
	#Se obtiene el id del tema actual 
	prueba2 = Temas.objects.filter(nombre=tema).values_list('id_tema', flat=True)
	ids_equipo_relacionado_tema = Temas.objects.get(id_tema__in=prueba2)
	#Se obtiene el equipo relacionado al usuario actual con el tema actual, esto para sacar el id de equipo
	id_equipo_relacionado_tema_count = Asignar.objects.get(id_equipo__in=ids_equipos_relacionados_usuario, id_tema=ids_equipo_relacionado_tema)
	#Se muestra equipo en tema actual
	hace_equipo = Hace.objects.filter(id_equipo__in=ids_equipos_relacionados_grupo, id_tema=ids_equipo_relacionado_tema)
	id_tema_voto = Temas.objects.get(nombre=tema).id_tema

	if request.method == 'POST':
		voto = request.POST.get("preguntaInicial")
		agregar_voto = Actividad.objects.filter(user=current_user, id_tema_id=id_tema_voto).update(voto=F('voto')+1)
		return redirect('AMCE:comentaPreguntaInicial', codigo=codigo, tema=tema)

	return render(request, 'estudiante/FeedPreguntaInicialHecha.html', {'hace_equipo':hace_equipo, 'codigo':codigo, 'tema':tema})

def comentaPreguntaInicial(request, tema, codigo):
	if request.method == 'POST':
		form = FormComentarPI(request.POST)
		if form.is_valid():
			print("es valido el form")
	else:
		form = FormComentarPI()

	return render(request, "estudiante/ComentarPreguntaInicial.html",{'form': form})

"""
	VISTAS/FUNCIONES DE PROFESOR
"""

def esProfesor(request):
	current_user = get_object_or_404(User, pk=request.user.pk)
	usuarioTipo = UserType.objects.filter(userType=current_user,flag=2)
	if( usuarioTipo ):
		return true
	else:
		return false

def profesor(request):
	current_user = get_object_or_404(User, pk=request.user.pk)
	usuarioTipo2 = UserType(userType=current_user,flag=2)
	usuarioTipo2.save()
	return redirect(to="AMCE:ProfMisGrupos")

@login_required
def ProfMisGrupos(request):
	#Se muestran los Grupos asignados al ID del usuario actual
	current_user = get_object_or_404(User, pk=request.user.pk)
	grupos = Grupos.objects.filter(user_id=request.user.pk)
	grupos = grupos[::-1]
	return render(request,"profesor/MisGrupos.html", {'grupos':grupos})

@login_required
def ProfCrearGrupo(request):
	current_user = get_object_or_404(User, pk=request.user.pk)
	grupos = Grupos.objects.filter(user_id=request.user.pk)
	if request.method == 'POST':
		form = FormCrearGrupo(request.POST)
		if form.is_valid():
			codigo = random_string(7)
			mismo_codigo = Grupos.objects.filter(codigo=codigo)
			while ( mismo_codigo.exists() ):
				codigo = random_string(7)
			print(form.cleaned_data['nombre'])
			nuevo_grupo = Grupos(codigo=codigo,
								grupo=form.cleaned_data['nombre'], 
								materia=form.cleaned_data['materia'], 
								institucion=form.cleaned_data['institucion'], 
								user_id=current_user)
			messages.add_message(request, messages.INFO, 'Grupo creado')
			nuevo_grupo.save()
			form = FormCrearGrupo()
			return redirect(reverse('AMCE:ProfPaginaGrupo',  args=[codigo]))
	else:
		form = FormCrearGrupo()
		return render(request, 'profesor/CrearGrupo.html', {'form': form})

@login_required
def ProfPaginaGrupo(request, codigo):
	current_user = get_object_or_404(User, pk=request.user.pk)
	grupo = Grupos.objects.filter(codigo=codigo)
	equipos = Equipos.objects.filter(codigo_materia_id=codigo)
	ids_equipos = equipos.values_list('id_equipo', flat=True)
	ids_temas = Asignar.objects.filter(id_equipo__in=ids_equipos).values_list('id_tema', flat=True)
	temas = Temas.objects.filter(id_tema__in=ids_temas)
	return render(request, 'profesor/PaginaGrupo.html', {'codigo':codigo, 'grupo':grupo[0], 'equipos':equipos, 'temas':temas})

@login_required
def ProfCrearEquipo(request, codigo):
	current_user = get_object_or_404(User, pk=request.user.pk)
	grupo = Grupos.objects.get(codigo=codigo)
	if request.method == 'POST':
		form = FormCrearEquipo(request.POST)
		if form.is_valid():
			nuevo_equipo = Equipos(nombre=form.cleaned_data['nombre'],
								   codigo_materia=grupo)
			nuevo_equipo.save()
			for integrante in form.cleaned_data['integrantes']:
				usuario = User.objects.get(id=integrante)
				nuevo_integrante = Pertenecer(id_equipo=nuevo_equipo,
											  user_id=usuario)
				nuevo_integrante.save()
			messages.add_message(request, messages.INFO, 'Equipo creado')
			form = FormCrearEquipo(codigo=codigo)
			return redirect(reverse('AMCE:ProfPaginaGrupo',  args=[codigo]))
	else:
		form = FormCrearEquipo(codigo=codigo)
		return render(request, 'profesor/CrearEquipo.html', {'codigo':codigo,'form': form})

@login_required
def ProfPaginaEquipo(request, codigo, equipo):
	current_user = get_object_or_404(User, pk=request.user.pk)
	equipo_nombre = Equipos.objects.get(id_equipo=equipo).nombre
	integrantes_ids = Pertenecer.objects.filter(id_equipo=equipo).values_list('user_id', flat=True)
	integrantes = User.objects.filter(id__in=integrantes_ids).values_list('last_name','first_name').order_by('last_name','first_name')
	integrantes_nombres = []
	for i in integrantes:
		integrantes_nombres.append(i[0] + " " + i[1])
	print(integrantes)
	return render(request, 'profesor/PaginaEquipo.html', {'equipo_nombre':equipo_nombre, 'integrantes':integrantes_nombres})

@login_required
def ProfAsignarTemaGrupo(request, codigo):
	current_user = get_object_or_404(User, pk=request.user.pk)
	grupo = Grupos.objects.get(codigo=codigo)
	if request.method == 'POST':
		form = AsignarTemaGrupo(request.POST)
		if form.is_valid():
			id_tema = form.cleaned_data['tema']
			for id_equipo in form.cleaned_data['equipos']:
				creado = Asignar.objects.filter(id_equipo=id_equipo,id_tema=id_tema)
				if not creado.exists():
					equipo = Equipos.objects.get(id_equipo=id_equipo)
					tema = Temas.objects.get(id_tema=id_tema)
					asignacion = Asignar(id_equipo=equipo,
										id_tema=tema)
					asignacion.save()
			messages.add_message(request, messages.INFO, 'Tema asignado')
			form = FormCrearEquipo(codigo=codigo)
			return redirect(reverse('AMCE:ProfPaginaGrupo',  args=[codigo]))
	else:
		form = AsignarTemaGrupo(codigo=codigo)
		return render(request, 'profesor/AsignarTemaGrupo.html', {'codigo':codigo,'form': form})

@login_required
def ProfTemaAsignado(request, codigo, tema):
	current_user = get_object_or_404(User, pk=request.user.pk)
	tema_info = Temas.objects.filter(id_tema=tema)
	grupo_info = Grupos.objects.filter(codigo=codigo)
	ids_equipos = Asignar.objects.filter(id_tema=tema).values_list('id_equipo', flat=True)
	equipos = Equipos.objects.filter(id_equipo__in=ids_equipos)
	print(equipos)
	return render(request, 'profesor/TemaAsignado.html', {'grupo':grupo_info[0], 'tema':tema_info[0], 'equipos':equipos})

@login_required
def ProfMisTemas(request):
	#Se muestran los Temas asignados al ID del usuario actual
	current_user = get_object_or_404(User, pk=request.user.pk)
	temas = Temas.objects.filter(user_id=request.user.pk)
	temas = temas[::-1]
	return render(request,"profesor/MisTemas.html", {'temas':temas})

@login_required
def ProfCrearTema(request):
	current_user = get_object_or_404(User, pk=request.user.pk)
	temas = Temas.objects.filter(user_id=request.user.pk)
	if request.method == 'POST':
		form = FormCrearTema(request.POST)
		if form.is_valid():
			nuevo_tema = Temas(nombre=form.cleaned_data['nombre'],
								user_id=current_user)
			messages.add_message(request, messages.INFO, 'Tema creado')
			nuevo_tema.save()
			form = FormCrearGrupo()
			return redirect(reverse('AMCE:ProfMisTemas'))
	else:
		form = FormCrearTema()
		return render(request, 'profesor/CrearTema.html', {'form': form})

#Función para generar el id de un Grupo cuando se crea
def random_string(char_num): 
	letter_count = random.randint(1, char_num-2)
	digit_count = char_num - letter_count
	str1 = ''.join((random.choice(string.ascii_lowercase) for x in range(letter_count)))  
	str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))  

	sam_list = list(str1) # it converts the string to list.  
	random.shuffle(sam_list) # It uses a random.shuffle() function to shuffle the string.  
	final_string = ''.join(sam_list)  
	return final_string
	