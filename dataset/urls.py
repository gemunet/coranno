from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

from . import views
from . import api

router = routers.DefaultRouter()
router.register(r'datasets', api.DatasetViewSet)
router.register(r'documents', api.DocumentViewSet)

urlpatterns = [
    path('', views.DatasetView.as_view(), name='datasets'),
    path('<int:pk>/docs', views.DocumentsView.as_view(), name='dataset_docs'),
    path('<int:pk>/upload', views.UploadView.as_view(), name='dataset_upload'),
    path('<int:pk>/download', views.DownloadView.as_view(), name='dataset_download'),
]