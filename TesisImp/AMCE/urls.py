from django.contrib import admin
from django.urls import include, path

#se agrega para heroku
#from django.conf import settings 
#from django.conf.urls.static import static

# Views
from AMCE import views

app_name = "AMCE"
urlpatterns = [
# URLS COMPARTIDAS
path('', views.index, name = 'index'),
path('registro/', views.registro, name = 'registro'),
path('bienvenida/', views.bienvenida, name = 'bienvenida'),
# URLS ESTUDIANTE
path('MG1/', views.MG1, name = 'MG1'),
path('crear/', views.MG1, name = 'crear'),
path('MG1/Grupo/<str:codigo>', views.PaginaAlumnoTema, name = 'PaginaAlumnoTema'),
path('MG1/UnirseGrupo/', views.AlumnoUnirseGrupo, name = 'AlumnoUnirseGrupo'),
path('MG1/Grupo/<str:codigo>/<str:tema>', views.PaginaActividadAlumno, name = 'PaginaActividadAlumno'),
path('MG1/Grupo/<str:codigo>/<str:tema>/PreguntaInicial', views.postPreguntaInicial, name = 'postPreguntaInicial'),
path('MG1/Grupo/<str:codigo>/<str:tema>/PreguntaInicial/Feed', views.feed, name = 'feed'), 
path('MG1/Grupo/<str:codigo>/<str:tema>/PreguntaInicial/FeedPreguntaInicial', views.feedPIHecha, name = 'feedPIHecha'),
# URLS PROFESOR
path('profesor/', views.profesor, name = 'profesor'),
path('profesor/MisGrupos/', views.ProfMisGrupos, name = 'ProfMisGrupos'),
path('profesor/CrearGrupo/', views.ProfCrearGrupo, name = 'ProfCrearGrupo'),
path('profesor/Grupo/<str:codigo>', views.ProfPaginaGrupo, name = 'ProfPaginaGrupo'),
path('profesor/Grupo/<str:codigo>/CrearEquipo', views.ProfCrearEquipo, name = 'ProfCrearEquipo'),
path('profesor/Grupo/<str:codigo>/Equipo/<int:equipo>', views.ProfPaginaEquipo, name = 'ProfPaginaEquipo'),
path('profesor/Grupo/<str:codigo>/AsignarTema', views.ProfAsignarTemaGrupo, name = 'ProfAsignarTemaGrupo'),
path('profesor/Grupo/<str:codigo>/<int:tema>', views.ProfTemaAsignado, name = 'ProfTemaAsignado'),
path('profesor/MisTemas/', views.ProfMisTemas, name = 'ProfMisTemas'),
path('profesor/CrearTema/', views.ProfCrearTema, name = 'ProfCrearTema')
]

