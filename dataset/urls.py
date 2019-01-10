from django.urls import path

from . import views

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),

    path('datasets', views.DatasetList.as_view(), name='dataset_list'),
    path('dataset/<int:pk>', views.DatasetDetail.as_view(), name='dataset_detail'),
    path('create', views.DatasetCreate.as_view(), name='dataset_create'),
    path('update/<int:pk>', views.DatasetUpdate.as_view(), name='dataset_edit'),
    path('delete/<int:pk>', views.DatasetDelete.as_view(), name='dataset_delete'),
]