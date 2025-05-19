from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AgrupamientoView,
    ArchivosList,
    ArchivoSubidoViewSet,
    ArchivoUploadView,
    ArticuloViewSet,
    ClusterViewSet,
    CoherenciaClustersView,
    EstadisticasView,
    GenerarBibView,
    Requerimiento3View,
)

router = DefaultRouter()
router.register(r"articulos", ArticuloViewSet)
router.register(r"clusters", ClusterViewSet)
router.register(r"archivos", ArchivoSubidoViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("subir/", ArchivoUploadView.as_view(), name="archivo-upload"),
]

urlpatterns += [
    path("estadisticas/", EstadisticasView.as_view(), name="estadisticas"),
]


urlpatterns += [
    path("generar_bib/", GenerarBibView.as_view(), name="generar_bib"),
]

urlpatterns += [path("categorias/", Requerimiento3View.as_view(), name="categorias")]
urlpatterns += [path("agrupamiento/", AgrupamientoView.as_view(), name="agrupamiento")]
urlpatterns += [
    path("coherencia/", CoherenciaClustersView.as_view(), name="coherencia_clusters")
]
urlpatterns += [path("archivos/", ArchivosList.as_view(), name="archivos-list")]
