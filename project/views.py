from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django import forms

from dataset.models import Dataset, Document
from .models import Project

class ProjectView(LoginRequiredMixin, CreateView): 
    model = Project
    fields = ['name', 'description', 'project_type', 'split_pattern', 'split_type', 'datasets']
    template_name = 'project/projects.html'
    success_url = reverse_lazy('projects')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.filter_annotation_ids = self.request.POST.get("filter_annotation_ids", None)
        return super(ProjectView, self).form_valid(form)

class LabelView(LoginRequiredMixin, TemplateView):
    template_name = 'project/label.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        context = super(LabelView, self).get_context_data(object_list=object_list, kwargs=kwargs)
        context['section'] = self.project.name
        return context

class ProjectDatasetView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['datasets']
    template_name = 'project/datasets.html'

    def get_success_url(self):
        return reverse_lazy('project_datasets', args=[self.kwargs['pk']])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProjectDatasetView, self).form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        context = super(ProjectDatasetView, self).get_context_data(object_list=object_list, kwargs=kwargs)
        context['section'] = self.project.name
        return context

class AnnotationView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return [project.get_template_name()]

    def get_context_data(self, *, object_list=None, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        context = super().get_context_data(object_list=object_list, kwargs=kwargs)
        context['section'] = self.project.name
        return context

class GuidelineView(LoginRequiredMixin, TemplateView):
    template_name = 'project/guideline.html'

class StatsView(LoginRequiredMixin, TemplateView):
    template_name = 'project/stats.html'

    def get_context_data(self, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        context = super().get_context_data(*args, **kwargs)
        context['project'] = self.project
        context['annotations'] = self.project.annotations.all().order_by('label_id')

        print(self.project.annotations.all())

        from collections import defaultdict
        #print(defaultdict(self.project.annotations.all()))
        #print(len(self.project.annotations.all()))
        return context