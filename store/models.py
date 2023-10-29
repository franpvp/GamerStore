from django.db import models
from django.contrib.auth import get_user_model 
from django.conf import settings


# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Juego(models.Model):
    codigo_invent= models.CharField(max_length=200, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='juegos/' , null=True , blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='juegos')
    precio = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return self.get_code_name()

    def get_code_name(self):
        return f" INF: {self.codigo_invent} - {self.nombre}"

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=settings.ROLES)

    def __str__(self):
        return self.user.username + ' - ' + self.role
    
class Carrito(models.Model):
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)