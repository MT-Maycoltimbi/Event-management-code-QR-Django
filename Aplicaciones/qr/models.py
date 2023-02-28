from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # identification = models.TextField(max_length=500, blank=True)
    roles = [
        ('admin', 'Administrador'),
        ('user', 'Usuario'),]
    role = models.CharField(max_length=10, choices=roles, default="user")
    cedula = models.CharField(max_length=10, default=0)
    age = models.PositiveIntegerField(default=0)
    sexos = [
        ('F', 'Femenino'),
        ('M', 'Masculino')
    ]
    sexo = models.CharField(max_length=1, choices=sexos, default='F')
    address = models.CharField(max_length=80, default=0)
    phone = models.PositiveIntegerField(max_length=10, default=0)
    op = [
        ('medios', 'medios impresos'),
        ('amigo', 'amigos'),
        ('redes', 'redes sociales')
    ]
    info = models.CharField(max_length=30, choices=op, default='amigo')
    data = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='codigos_qr/')

class Eventos(models.Model):
    id_evento = models.AutoField(primary_key=True )
    name_evento = models.CharField(max_length=50, default=0)
    ubicacion = models.CharField(max_length=80, default=0)
    tipo_evento = models.CharField(max_length=50, default=0)
    responsable = models.CharField(max_length=30, default=0)
    requisitos = models.CharField(max_length=100, default=0)
    contacto = models.PositiveIntegerField(max_length=10, default=0)
    fecha_evento =  models.CharField(max_length=20)
    hora_evento = models.CharField(max_length=20)
    cupos = models.PositiveIntegerField(default=10)
    descripcion = models.CharField(max_length=300, default=0)
    enlace = models.CharField(max_length=100)
    mi_lista = ArrayField(models.CharField(max_length=500), default=list)
        

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# @receiver(post_save, sender=User)
# def create_data_evento(sender, instance, created, **kwargs):
#     if created:
#         Eventos.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_data_evento(sender, instance, **kwargs):
#     instance.eventos.save()
#segunda base para eventos