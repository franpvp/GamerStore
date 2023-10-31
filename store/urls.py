from django.urls import path
from .views import home, login ,index, registro, eliminar_usuario, editar_datos, principal, listado_usuarios, terror, accion, aventura, carreras, supervivencia, ver_carrito, pago, eliminar_del_carrito, agregar_al_carrito, listado_juegos, crear_juego, juegos_show, eliminar_juego, juegos_editar, logout_view, recuperar_contrasenna
urlpatterns = [
    # link Juegos
    path('princjuegos/principal', principal, name='principal'),
    path('princjuegos/juegosterror', terror, name="terror"),
    path('princjuegos/juegosaventura', aventura, name="aventura"),
    path('princjuegos/juegosaccion', accion, name="accion"),
    path('princjuegos/juegoscarreras', carreras, name="carreras"),
    path('princjuegos/juegossupervivencia', supervivencia, name="supervivencia"),
    path('princjuegos/ver_carrito', ver_carrito, name="ver_carrito"),
    path('princjuegos/pago', pago, name="pago"),
    path('princjuegos/agregar_al_carrito/<int:juego_id>/', agregar_al_carrito, name="agregar_al_carrito"),
    path('princjuegos/listado_juegos', listado_juegos, name="listado_juegos"),
    path('princjuegos/crearjuego', crear_juego, name="crear_juego"),
    path('princjuegos/<int:id>/editarjuego', juegos_editar, name="juegos_editar"),
    path('princjuegos/<int:id>/juego_show', juegos_show, name="juegos_show"),
    path('princjuegos/<int:id>/eliminar_juego', eliminar_juego, name="eliminar_juego"),
    path('eliminar_del_carrito/<int:juego_id>/', eliminar_del_carrito, name="eliminar_del_carrito"),
    

    # link enlace formularios usuario
    path('inicio_sesion/', login, name="inicio_sesion"),
    path('home/', home, name="home"),
    path('registro/', registro, name="registro"),
    path('eliminar_usuario/<int:id>/', eliminar_usuario, name="eliminar_usuario"),
    path('editar_datos/<int:id>/', editar_datos, name="editar_datos"),
    path('', index, name="index"),
    path('recuperar_contrasenna/', recuperar_contrasenna, name="recuperar_contrasenna"),
    path('princjuegos/listado_usuarios/', listado_usuarios, name="listado_usuarios"),
    path('logout/', logout_view, name="logout")

]