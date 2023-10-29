from django.shortcuts import render, get_object_or_404, redirect
from .models import Juego, Categoria , UserProfile , Carrito 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import role_requiered
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

# definicion sesion de usuarios y perfil
def index(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        clave = request.POST.get('pass')

        user = authenticate(request, username = usuario, password = clave)
        if user is not None:
            # Autenticación exitosa
            login(request, user)
            try:
                profile = user.userprofile  # Obtén el perfil de usuario
                request.session['perfil'] = profile.role
            except UserProfile.DoesNotExist:
                # Si el perfil de usuario no existe, puedes manejarlo aquí
                messages.error(request, 'El perfil de usuario no está configurado correctamente.')
                return redirect('principal')
            
            return redirect('listado_juegos')
        else:
            context = {
                'error': 'Error, inténtelo nuevamente'
            }
            return render(request, 'auth/index.html', context)

    return render(request, 'auth/index.html')

    
@login_required
def listado_usuarios(request):

    users = User.objects.all()
    perfil = request.session.get('perfil') # perfil es el rol, "cliente" o "admin"
    context = {
        'user': users,
        'perfil': perfil,
    }

    return render(request, 'auth/listado_usuarios.html', context)
    
def registro(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        # Validar los datos ingresados 
        if not username:
            messages.error(request, 'Nombre de usuario es obligatorio')
            return redirect('registro')
        
        if len(password) < 6 or len(password) > 16:
            messages.error(request, 'La contraseña debe tener entre 6 y 16 caracteres')
            return redirect('registro')
        
        if not any(char.isupper() for char in password):
            messages.error(request, 'La contraseña debe contener al menos una letra mayúscula')
            return redirect('registro')

        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso')
            return redirect('registro')
        
        if password != password2:
            messages.error(request, 'La contraseña debe ser iguales')
            return redirect('registro')
        
        user = User.objects.create_user(
            first_name=first_name,
            username=username,
            password=password,
            email=email
        )
        # Se asigna rol cliente siempre al registrarse
        role = 'cliente'
        UserProfile.objects.create(user=user, role=role)

        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user:
            login(request, authenticated_user)

        messages.success(request, 'Se ha creado la cuenta correctamente como cliente')

        return redirect('listado_usuarios')
        
    else:
        return render(request, 'auth/registro.html')  
    
@role_requiered('admin')
def editar_datos(request,id):
    
        usuario = get_object_or_404(User, id=id)
        
        if request.method == 'POST':
            first_name = request.POST['first_name']
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            role = request.POST['role'] 

            usuario.first_name = first_name
            usuario.username = username
            usuario.set_password(password)
            usuario.email = email
            usuario.userprofile.role = role
            usuario.userprofile.save()  
            usuario.save()

            messages.success(request, 'Usuario editado exitosamente.')
            return redirect('listado_usuarios')
        return render(request, 'auth/editar_datos.html', {'usuario': usuario})


def recuperar_contrasenna(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        new_pass= "123123"

        try:
            usuario = User.objects.get(email=correo)
            usuario.set_password(new_pass)
            usuario.save()
            messages.success(request, 'La contraseña se actualizo con exito')
            return redirect('index')
        except User.DoesNotExist:
            messages.error(request,'No se encontro ningun usuario con ese correo Electronico')

    return render(request, 'auth/recuperar_contrasenna.html')

@role_requiered('admin')
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    usuario.delete()
    messages.success(request, 'Se ha Eliminado Correctamente')
    return redirect('listado_usuarios')
    
# Vista para cerrar sesión a un Usuario
def logout_view(request):
    print("Cierre de sesión solicitado")
    logout(request)
    request.session.flush() 
    return redirect('index')

# definiciones para juegos 
@login_required
def principal(request):
    return render(request, 'juegos/principal.html')

@login_required
def accion(request):
        
    juegos_accion = Juego.objects.filter(categoria__nombre='ACCION')
    perfil = request.session.get('perfil')
    context = {
        'juegos_accion': juegos_accion,
        'perfil': perfil,
    }
    return render(request, 'juegos/accion.html',context)
@login_required
def supervivencia(request):

    juegos_supervivencia = Juego.objects.filter(categoria__nombre='SUPERVIVENCIA')
    perfil = request.session.get('perfil')
    context = {
        'juegos_supervivencia': juegos_supervivencia,
        'perfil': perfil,
    }
    return render(request, 'juegos/supervivencia.html', context)
@login_required
def terror(request):

    juegos_terror = Juego.objects.filter(categoria__nombre='TERROR')
    perfil = request.session.get('perfil')
    context = {
        'juegos_terror': juegos_terror,
        'perfil': perfil,
    }
    return render(request, 'juegos/terror.html',context)
@login_required
def aventura(request):

    juegos_aventura = Juego.objects.filter(categoria__nombre='AVENTURA')
    perfil = request.session.get('perfil')
    context = {
        'juegos_aventura': juegos_aventura,
        'perfil': perfil,
    }
    return render(request, 'juegos/aventura.html',context)
@login_required
def carreras(request):

    juegos_carreras = Juego.objects.filter(categoria__nombre='CARRERAS')
    perfil = request.session.get('perfil')
    context = {
        'juegos_carreras': juegos_carreras,
        'perfil': perfil,
    }
    return render(request, 'juegos/carreras.html',context)

@login_required
def agregar_al_carrito(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if Carrito.objects.filter(usuario=user_profile, juego=juego).exists():
        carrito_item = Carrito.objects.get(usuario=user_profile, juego=juego)
        carrito_item.cantidad += 1
        carrito_item.save()
    else:
        Carrito.objects.create(usuario=user_profile, juego=juego)
    
    return HttpResponseRedirect(reverse('listado_juegos'))

@login_required
def ver_carrito(request):
    user_profile = None
    carrito = []

    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            carrito = Carrito.objects.filter(usuario=user_profile)
        except UserProfile.DoesNotExist:
            pass

    if carrito is not None:
        total = sum(item.juego.precio * item.cantidad for item in carrito)
    else:
        total = 0
    context = {
            'carrito': carrito,
            'perfil': user_profile,
            'total': total
        }
    
    return render(request, 'juegos/ver_carrito.html', context)

@login_required
def eliminar_del_carrito(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    
    Carrito.objects.filter(usuario=request.user.userprofile, juego=juego).delete()
    

   
    return redirect('ver_carrito')

@login_required
def pago(request):
    return render(request, 'juegos/pago.html')

@login_required
def juegos_show(request, id):
    juego = get_object_or_404(Juego, id=id)
    context = {
        'juego' : juego
         }

    return render(request, 'juegos/juegos_show.html',context)

@login_required
def listado_juegos (request):
    juegos = Juego.objects.all()

    perfil = request.session.get('perfil')

    context ={
        'juegos' : juegos,
        'perfil' : perfil
    }
    return render (request, 'juegos/listado_juegos.html',context)

@role_requiered('admin')
def juegos_editar(request,id):
    juego = get_object_or_404(Juego, id=id)
    
    if request.method =='POST':
        categoria_id = request.POST.get ('categoria')
        categoria = get_object_or_404(Categoria, id=categoria_id)    

        juego.nombre = request.POST['nombre']
        juego.codigo= request.POST['codigo_invent']
        juego.descripcion = request.POST['descripcion']
        juego.categoria = categoria
        nuevo_precio = request.POST.get('nuevo_precio')
        if nuevo_precio is not None:
            juego.precio = nuevo_precio
        if 'imagen' in request.FILES:
            juego.imagen = request.FILES['imagen']
        
        juego.save()
        messages.success(request, 'Se ha Actualizado Correctamente')

    
    categorias =Categoria.objects.all()
    context ={
        'juego' : juego,
        'categorias' : categorias
    }
    return render(request, 'juegos/juegos_editar.html', context)

@role_requiered('admin')
def crear_juego (request): 

    if request.method =='POST':
        categoria_id = request.POST.get ('categoria')
        categoria = get_object_or_404(Categoria, id=categoria_id)
        
        codigo_invent = request.POST.get('codigo_invent')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
        precio = request.POST.get('precio')

        if float(precio) > 0:
            Juego.objects.create(
                codigo_invent=codigo_invent,
                nombre=nombre,
                descripcion=descripcion,
                imagen=imagen,
                categoria=categoria,
                precio = precio
            )
            messages.success(request, 'Se ha creado Correctamente')
            return redirect('listado_juegos')
        else:
            messages.error(request, 'El precio debe ser mayor que 0')

    categorias = Categoria.objects.all()
    
    contexto = {
        'categorias': categorias
    }
    
    return render (request, 'juegos/crearjuego.html', contexto)

@role_requiered('admin')
def eliminar_juego (request, id):
    juego = get_object_or_404(Juego, id=id)
    juego.delete()
    messages.success(request, 'Se ha Eliminado Correctamente')
    return redirect('listado_juegos')
