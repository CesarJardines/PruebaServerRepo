# Generated by Django 3.2.5 on 2022-01-05 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id_actividad', models.AutoField(primary_key=True, serialize=False)),
                ('contenido', models.TextField()),
                ('hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('pasoMG', models.FloatField(blank=True, default=None, null=True)),
                ('voto', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Equipos',
            fields=[
                ('id_equipo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Grupos',
            fields=[
                ('codigo', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('grupo', models.CharField(max_length=100)),
                ('materia', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('institucion', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag', models.IntegerField(choices=[(1, 'Student'), (2, 'Teacher')], default=1)),
                ('userType', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Temas',
            fields=[
                ('id_tema', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Pertenecer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AMCE.equipos')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inscribir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AMCE.grupos')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField(default='')),
                ('id_actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AMCE.actividad')),
                ('id_equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AMCE.equipos')),
                ('id_tema', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='AMCE.temas')),
            ],
        ),
        migrations.AddField(
            model_name='equipos',
            name='codigo_materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AMCE.grupos'),
        ),
        migrations.CreateModel(
            name='Asignar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AMCE.equipos')),
                ('id_tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AMCE.temas')),
            ],
        ),
        migrations.AddField(
            model_name='actividad',
            name='id_tema',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='AMCE.temas'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
