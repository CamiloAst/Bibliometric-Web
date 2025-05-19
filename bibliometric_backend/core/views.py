import os

import pandas as pd
from django.conf import settings
from django.shortcuts import render

# Create your views here.
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ArchivoSubido, Articulo, Cluster
from .serializers import ArchivoSubidoSerializer, ArticuloSerializer, ClusterSerializer
from .utils.bibtools import procesar_archivos_csv_para_bib
from .utils.categorias import procesar_categorias_y_nubes
from .utils.clustering import cluster_abstracts
from .utils.coherencia import analizar_coherencia
from .utils.estadisticas import generar_estadisticas_completas
from .utils.limpieza import procesar_archivo_csv


class ArticuloViewSet(viewsets.ModelViewSet):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer


class ArchivoSubidoViewSet(viewsets.ModelViewSet):
    queryset = ArchivoSubido.objects.all()
    serializer_class = ArchivoSubidoSerializer


class ArchivoUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        serializer = ArchivoSubidoSerializer(data=request.data)
        if serializer.is_valid():
            archivo_guardado = serializer.save()
            ruta = archivo_guardado.archivo.path

            # Lógica de ejemplo: carga si es CSV
            if ruta.endswith(".csv"):
                df = pd.read_csv(ruta)
                if ruta.endswith(".csv"):
                    limpio, duplicados = procesar_archivo_csv(ruta)
                    print(f"✅ Limpio: {limpio}")
                    print(f"⚠️  Duplicados: {duplicados}")

            return Response(
                {"mensaje": "Archivo recibido y procesado."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EstadisticasView(APIView):
    def get(self, request):
        nombre = request.GET.get("archivo")
        if not nombre:
            return Response({"error": "Falta el parámetro 'archivo'"}, status=400)

        archivo = f"media/archivos/{nombre}.csv"
        out_dir = f"media/resultados/{nombre}/estadisticas"

        try:
            ruta_resultados = generar_estadisticas_completas(
                archivo, output_dir=out_dir
            )

            # Listar archivos generados
            archivos_generados = os.listdir(out_dir)

            return Response(
                {
                    "mensaje": "Estadísticas generadas",
                    "carpeta": ruta_resultados,
                    "archivos": archivos_generados,  # ⬅️ Aquí te muestra qué se generó
                }
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class GenerarBibView(APIView):
    def get(self, request):
        nombre = request.GET.get("archivo")
        if not nombre:
            return Response({"error": "Falta el parámetro 'archivo'"}, status=400)

        archivo = f"media/archivos/"
        out_dir = f"media/resultados/{nombre}/bibtex"
        try:
            print("Procesando archivo:", archivo)
            print("Guardando en:", out_dir)
            resultados = procesar_archivos_csv_para_bib(archivo, out_dir)
            return Response(resultados, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class Requerimiento3View(APIView):
    def get(self, request):
        nombre = request.GET.get("archivo")
        if not nombre:
            return Response({"error": "Falta el parámetro 'archivo'"}, status=400)

        archivo = f"media/archivos/{nombre}.csv"
        out_dir = f"media/resultados/{nombre}/categorias"
        try:
            resultado = procesar_categorias_y_nubes(archivo, out_dir)
            return Response(
                {
                    "categorias": resultado["categorias"],
                    "imagenes": resultado["archivos_generados"],
                }
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class AgrupamientoView(APIView):
    def get(self, request):
        nombre = request.GET.get("archivo")
        if not nombre:
            return Response({"error": "Falta el parámetro 'archivo'"}, status=400)

        archivo = f"media/archivos/{nombre}.csv"
        out_dir = f"media/resultados/{nombre}/agrupamiento"  # ajustar si es necesario
        try:
            resultado = cluster_abstracts(archivo, out_dir)
            return Response(resultado, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class CoherenciaClustersView(APIView):
    def get(self, request):
        nombre = request.GET.get("archivo")
        if not nombre:
            return Response({"error": "Falta el parámetro 'archivo'"}, status=400)

        archivo = f"media/archivos/{nombre}.csv"
        out_dir = f"media/resultados/{nombre}/coherencia"  # Ajusta si es otro
        try:
            resultado = analizar_coherencia(archivo, out_dir)
            return Response(resultado, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ArchivosList(APIView):
    def get(self, request):
        carpeta = os.path.join(settings.MEDIA_ROOT, "archivos")
        archivos = []

        if os.path.exists(carpeta):
            for archivo in os.listdir(carpeta):
                if archivo.endswith(".csv"):
                    nombre = os.path.splitext(archivo)[0]  # quita ".csv"
                    archivos.append(nombre)  # <-- solo el nombre, no la ruta

        return Response(archivos)
