from rest_framework import serializers
from .models import Articulo, Cluster, ArchivoSubido


class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = "__all__"


class ClusterSerializer(serializers.ModelSerializer):
    articulos = ArticuloSerializer(many=True, read_only=True)

    class Meta:
        model = Cluster
        fields = "__all__"


class ArchivoSubidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivoSubido
        fields = "__all__"
