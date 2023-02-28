from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Profile, Eventos
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
import matplotlib.pyplot as plt
import io
import qrcode
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile


def grafico_barras(request):
    usuarios = User.objects.all().select_related('profile')
    x = [usuario.profile.age for usuario in usuarios]
    y = [usuario.profile.sexo for usuario in usuarios]
    plt.bar(x, y)
    plt.title("Gráfico de barras")
    plt.xlabel("Edad")
    plt.ylabel("Sexo")
    plt.show()
    return render(request, 'charts.html')


# Create your views here.
def isAdmin(request):
    return request.user.profile.role == "admin"

@login_required
def home(request):
    return render(request, "home.html")
    
@login_required
def Inscripciones(request):
    if isAdmin(request):
        return render(request, 'inscripciones.html')
    else:
        return render(request, 'error_404.html')

@login_required
def crear_evento(request):
    if isAdmin(request):
        if request.method == "GET":
            return render(request, "crear-event.html")
            
        else:
            evento_name = request.POST['evento_name']
            ubicacion = request.POST['ubicacion']
            tipo_evento = request.POST['tipo_evento']
            responsable = request.POST['responsable']
            requisitos = request.POST['requisitos']
            contacto = request.POST['contacto']
            fecha_evento = request.POST['fecha_evento']
            hora_evento = request.POST['hora_evento']
            cupos = request.POST['cupos']
            descripcion = request.POST['descripcion']
            evento = Eventos()
            evento.name_evento = evento_name
            evento.ubicacion=ubicacion
            evento.tipo_evento=tipo_evento
            evento.responsable=responsable
            evento.requisitos=requisitos
            evento.contacto=contacto
            evento.fecha_evento=fecha_evento
            evento.hora_evento=hora_evento
            evento.cupos=cupos
            evento.descripcion=descripcion 
            evento.save()
            return render(request, "crear-event.html", {"evento":evento})
    else:
        return render(request, 'error_404.html')

def editar_evento(request, id_evento):
    letras = 0
    for i in str(id_evento):
        if i not in "1234567890":
            letras += 1
    condicion = letras == 0

    if not(isAdmin(request)) or not(condicion) :
        return render(request, 'error_404.html')

    
    else:
        
        if request.method == "GET":
            eventos = Eventos.objects.get(id_evento=id_evento)
            return render(request, 'editar_evento.html', {"evento":eventos})
        else:
            evento_name = request.POST['evento_name']
            ubicacion = request.POST['ubicacion']
            tipo_evento = request.POST['tipo_evento']
            responsable = request.POST['responsable']
            requisitos = request.POST['requisitos']
            contacto = request.POST['contacto']
            fecha_evento = request.POST['fecha_evento']
            hora_evento = request.POST['hora_evento']
            cupos = request.POST['cupos']
            descripcion = request.POST['descripcion']
            id = request.POST["id_evento"]
            evento = Eventos.objects.get(id_evento=id)
            evento.name_evento = evento_name
            evento.ubicacion=ubicacion
            evento.tipo_evento=tipo_evento
            evento.responsable=responsable
            evento.requisitos=requisitos
            evento.contacto=contacto
            evento.fecha_evento=fecha_evento
            evento.hora_evento=hora_evento
            evento.cupos=cupos
            evento.descripcion=descripcion 
            evento.save()
            return redirect('gestion:event_creado')
    
    
@login_required
def event_creado(request):
    if isAdmin(request):
        if request.method == "GET":
            evento = Eventos.objects.all()
            
            return render(request, "event_creado.html", {"evento":evento})
        
    else:
        return render(request, 'error_404.html')

def eliminar_evento(request, id_evento):
    evento = Eventos.objects.get(id_evento=id_evento)
    evento.delete()
    return redirect('gestion:event_creado')

def registro_usuario(request, nombre):
    if request.method == "GET":
        return render(request, 'registro_usuario.html')
    else:
        try:
                        
            cedula = request.POST['txtcedula']
            name = request.POST.get('txtname', '')
            apellido = request.POST['txtlname']
            email = request.POST['txtemail']
            address = request.POST['txtad']
            sexo = request.POST['txtsex']
            age = request.POST['txtage']
            phone = request.POST['txtphone']
            info = request.POST['txtinfo']
            prueba = User.objects.all()
            t,identificador= '',0
            for usu in prueba:
                if usu.username == name+apellido+str(phone):
                    t += 'ya exite'
                    identificador = usu.id
            c =  t == 'ya exite'
            if c :
                evento = Eventos.objects.get(name_evento=nombre)
                mi_lista = evento.mi_lista
                mi_lista.append(identificador)
                evento.save()
                usuario = User.objects.get(id=identificador)

                asunto = "invitacion -"+str(name) 
                mensaje = "gracias por regristrate al evento "+nombre+"\n \npresenta este qr para ingresar al evento\n"
                email_desde = settings.EMAIL_HOST_USER
                email_para = [email]
                send_mail(asunto, mensaje, email_desde, email_para,fail_silently=False)

                evento = {}
                evento["evento"]=nombre
                return render(request, "confirmar_datos.html", {'usuario':usuario,'evento':evento})
            else: 
                usuario = User.objects.create_user(
                username=name+apellido+str(phone), first_name=name, last_name=apellido, email=email)
                usuario.profile.address = address
                usuario.profile.cedula = cedula
                usuario.profile.sexo = sexo
                usuario.profile.age = age
                usuario.profile.phone = phone
                usuario.profile.info = info
                data = str(cedula)+str(sexo)+str(usuario.id)+str(usuario.username)
                # Crear un objeto QRCode
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(data)
                qr.make(fit=True)

                # Crear una imagen PIL del código QR
                img = qr.make_image(fill_color="black", back_color="white")

                # Convertir la imagen PIL en bytes
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)

                # Crear un objeto de archivo cargado en memoria con los bytes
                file = InMemoryUploadedFile(img_bytes, None, 'codigo_qr.png', 'image/png', img_bytes.getbuffer().nbytes, None)

                # Guardar el archivo en el campo de imagen de un modelo de base de datos
                usuario.profile.data = data
                usuario.profile.imagen.save('codigo_qr.png', ContentFile(file.read()))


                # Devolver la imagen en la respuesta HTTP
                #return HttpResponse(img_bytes.getvalue(), content_type="image/png")
                usuario.save()

                evento = Eventos.objects.get(name_evento=nombre)
                mi_lista = evento.mi_lista
                mi_lista.append(usuario.id)
                evento.save()

                asunto = "invitacion -"+str(name) 
                mensaje = "gracias por regristrate al evento "+nombre+"\n \npresenta este qr para ingresar al evento\n"
                email_desde = settings.EMAIL_HOST_USER
                email_para = [email]
                send_mail(asunto, mensaje, email_desde, email_para,fail_silently=False)

                evento = {}
                evento["evento"]=nombre
                return render(request, "confirmar_datos.html", {'usuario':usuario,'evento':evento})
        except:
            return render(request, "error_404.html" )


def confirmar_datos(request):
    if request.method == "GET":
        usuarios = User.objects.all().select_related('profile')
        return render(request, 'confirmar_datos.html', {"usuario":usuarios})
    else:
        
        return render(request, "usuario.html")


def datos(request, id, nombre):
    try: 
        usuario = User.objects.get(id=id)
        condicion = str(id)==str(usuario.id) and str(usuario.first_name)==str(nombre)
        if condicion:
            return render(request, "usuario.html", {"usuario": usuario})
        else:
            return render(request,"error_404.html" )
    except:
        return render(request,"error_404.html" )



@login_required
def autent_qr(request):
    if isAdmin(request):
        return render(request, "autent_qr.html")
    else:
        return render(request, 'error_404.html')



@login_required
def dashboard(request):
    if isAdmin(request):
        return render(request, "index.html")
    else:
        return render(request, 'error_404.html')


@login_required
def charts(request):
    if isAdmin(request):
        data = {}
        n_usuarios = User.objects.all().count()
        usuarios= User.objects.all().select_related('profile')
        w,m,unico,cantidad = 0,0,[],[]
        for i in usuarios:
            if i.profile.sexo == "F":
                w += 1
                if i.profile.info not in unico:
                    unico.append(i.profile.info)
                    cantidad.append(1)
                else:
                    ind = unico.index(i.profile.info)
                    cantidad[ind] += 1
            elif i.profile.sexo == "M":
                m += 1
                if i.profile.info not in unico:
                    unico.append(i.profile.info)
                    cantidad.append(1)
                else:
                    ind = unico.index(i.profile.info)
                    cantidad[ind] += 1
          
        data['n_usuarios'],data['women'],data['men'] = n_usuarios,w,m
        return render(request, "charts.html", {"data": data,})
    else:
        return render(request, 'error_404.html')



@login_required
def Inscripciones(request):
    if request.method == "GET":
        usuarios = User.objects.all().select_related('profile')
        return render(request, "inscripciones.html", {"usuario":usuarios})


    
@login_required
def edicion(request, id):
    usuario = User.objects.get(id=id)
    return render(request, "editar.html", {"usuario": usuario})

@login_required
def editar(request):
    try:
        name = request.POST["txtname"]
    except KeyError:
        name = "Anonymous"
            
    try:
        cedula = request.POST['txtcedula']
    except KeyError:
        cedula = 0

    try:
        apellido = request.POST['txtlname']
    except KeyError:
        apellido = "Anonymous"

    try:
        email = request.POST['txtemail']
    except KeyError:
        email = "Anonymous"

    try:
        address = request.POST['txtad']
    except KeyError:
        address = "Anonymous"
    
    try:
       role = request.POST['txtrol']
    except KeyError:
        role = "user"

    try:
        sexo = request.POST['txtsex']
    except KeyError:
        sexo = "F"

    try:
        age = request.POST['txtage']
    except KeyError:
        age = 0

    try:
        phone = request.POST['txtphone']
    except KeyError:
        phone = 0
    
    try:
        info = request.POST['txtinfo']
    except KeyError:
        info = "amigo"
    

    id = request.POST["txtid"]
    usuario = User.objects.get(id=id)
    usuario.first_name = name
    usuario.last_name = apellido
    usuario.email = email
    usuario.profile.address = address
    usuario.profile.cedula = cedula
    usuario.profile.role = role
    usuario.profile.sexo = sexo
    usuario.profile.age = age
    usuario.profile.phone = phone
    usuario.profile.info = info
    usuario.save()
    return redirect('gestion:dashboard')

@login_required
def eliminar(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    return redirect('gestion:Inscripciones')




def signup(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form': UserCreationForm})
    else:
        
        usuarios= User.objects.all().select_related('profile')
        valor = 0
        for i in usuarios:
            if i.profile.role == "admin":
                valor += 1
        if (request.POST['password1'] == request.POST['password2']) and valor<2 :
            try:
                usuario = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                usuario.profile.role = "admin"
                usuario.save()
                login(request, usuario)
                
                if(usuario.profile.role == "admin"):
                    return redirect('gestion:dashboard')
                else:     
                    url = reverse("gestion:datos", args=[usuario.id])
                    return redirect(url)
            except IntegrityError:
                return render(request, 'register.html', {
                    'form': UserCreationForm,
                    'error': 'usuario ya existe'})
        return render(request, 'register.html', {
            'form': UserCreationForm,
            'error': 'contraseñas no coinciden o ya están registrados un maximo de dos administradores'})


def signout(request):
    logout(request)
    return redirect('gestion:signin')


def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {"form": AuthenticationForm })
    else:
        usuario = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if usuario is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña inexistentes o invalidos'})
        else:
            login(request, usuario)
            if(usuario.profile.role == "admin"):
                return redirect('gestion:dashboard')
            else:     
                url = reverse("gestion:datos", args=[usuario.id])
                return redirect(url)


def error_404_view(request, exception):
    return render(request, 'error_404.html')


def mi_vista(request):
    return render(request, "error_404.html" )

