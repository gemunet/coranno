from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

from . import views
from . import api

router = routers.DefaultRouter()
router.register(r'projects', api.ProjectViewSet)
router.register(r'labels', api.LabelViewSet)
router.register(r'annotations', api.AnnotationViewSet)

urlpatterns = [
    path('', views.ProjectView.as_view(), name='projects'),
    path('<int:pk>/labels', views.LabelView.as_view(), name='project_labels'),
    path('<int:pk>/datasets', views.ProjectDatasetView.as_view(), name='project_datasets'),

    path('<int:pk>/annotation', views.AnnotationView.as_view(), name='project_annotation'),
    path('<int:pk>/docs/', api.DocumentList.as_view(), name='docs'),
    path('<int:pk>/docs/<int:doc_id>/annotations/', api.AnnotationList.as_view(), name='annotations'),
    path('<int:pk>/docs/<int:doc_id>/annotations/<int:annotation_id>', api.AnnotationDetail.as_view(), name='ann'),
]