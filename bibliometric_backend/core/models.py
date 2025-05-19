from django.db import models


class Articulo(models.Model):
    titulo = models.TextField()
    resumen = models.TextField()
    autores = models.TextField()
    año = models.IntegerField()
    tipo = models.CharField(max_length=100)
    fuente = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo[:50]


class Cluster(models.Model):
    nombre = models.CharField(max_length=100)
    articulos = models.ManyToManyField(Articulo)


class ArchivoSubido(models.Model):
    archivo = models.FileField(upload_to="archivos/")
    tipo = models.CharField(max_length=50)  # "Original" o "Duplicado"
    fecha = models.DateTimeField(auto_now_add=True)
