# Generated by Django 4.1.6 on 2023-02-27 04:31

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Eventos',
            fields=[
                ('id_evento', models.AutoField(primary_key=True, serialize=False)),
                ('name_evento', models.CharField(default=0, max_length=50)),
                ('ubicacion', models.CharField(default=0, max_length=80)),
                ('tipo_evento', models.CharField(default=0, max_length=50)),
                ('responsable', models.CharField(default=0, max_length=30)),
                ('requisitos', models.CharField(default=0, max_length=100)),
                ('contacto', models.PositiveIntegerField(default=0)),
                ('fecha_evento', models.CharField(max_length=20)),
                ('hora_evento', models.CharField(max_length=20)),
                ('cupos', models.PositiveIntegerField(default=10)),
                ('descripcion', models.CharField(default=0, max_length=300)),
                ('enlace', models.CharField(max_length=100)),
                ('mi_lista', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('admin', 'Administrador'), ('user', 'Usuario')], default='user', max_length=10)),
                ('cedula', models.CharField(default=0, max_length=10)),
                ('age', models.PositiveIntegerField(default=0)),
                ('sexo', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], default='F', max_length=1)),
                ('address', models.CharField(default=0, max_length=80)),
                ('phone', models.PositiveIntegerField(default=0)),
                ('info', models.CharField(choices=[('medios', 'medios impresos'), ('amigo', 'amigos'), ('redes', 'redes sociales')], default='amigo', max_length=30)),
                ('data', models.CharField(max_length=255)),
                ('imagen', models.ImageField(upload_to='codigos_qr/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]