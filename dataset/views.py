from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Dataset

class DatasetList(ListView): 
    model = Dataset

class DatasetDetail(DetailView): 
    model = Dataset

class DatasetCreate(CreateView): 
    model = Dataset
    fields = ['name']
    success_url = reverse_lazy('dataset_list')

class DatasetUpdate(UpdateView): 
    model = Dataset
    fields = ['name']
    success_url = reverse_lazy('dataset_list')

class DatasetDelete(DeleteView): 
    model = Dataset
    success_url = reverse_lazy('dataset_list')
