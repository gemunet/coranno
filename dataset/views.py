from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime
from io import TextIOWrapper
from .models import Dataset, Document
from project.models import Annotation

class DatasetView(LoginRequiredMixin, CreateView): 
    model = Dataset
    fields = ['name', 'description']
    template_name = 'dataset/datasets.html'
    success_url = reverse_lazy('datasets')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DatasetView, self).form_valid(form)

class DocumentsView(LoginRequiredMixin, ListView):
    model = Document
    fields = ['text', 'file', 'created_at']
    template_name = 'dataset/documents.html'
    paginate_by = 5

    def get_queryset(self):
        self.dataset = get_object_or_404(Dataset, pk=self.kwargs['pk'])
        return Document.objects.filter(dataset=self.dataset)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DocumentsView, self).get_context_data(object_list=object_list, kwargs=kwargs)
        context['section'] = self.dataset.name
        return context

    def render_to_response(self, context):
        if not self.object_list:
            return redirect('dataset_upload', pk=self.kwargs['pk'])
        else:
            return super(DocumentsView, self).render_to_response(context)


class UploadView(LoginRequiredMixin, TemplateView):
    template_name = 'dataset/upload.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        dataset = get_object_or_404(Dataset, pk=kwargs.get('pk'))
        context = super(UploadView, self).get_context_data(kwargs=kwargs)
        context['section'] = dataset.name
        return context

    def post(self, request, *args, **kwargs):
        dataset = get_object_or_404(Dataset, pk=kwargs.get('pk'))
        import_format = request.POST['format']

        try:
            if import_format == 'csv':
                form_data = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
                Document.objects.bulk_create([
                    Document(text=line.strip(), file=request.FILES['file'].name, dataset=dataset)
                    for line in form_data
                ])


            elif import_format == 'json':
                form_data = request.FILES['file'].file
                json_data = [json.loads(entry.decode('utf-8')) for entry in form_data]
                Document.objects.bulk_create([
                    Document(text=data['text'], file=data.get('file', request.FILES['file'].name), dataset=dataset)
                    for data in json_data
                ])

            elif import_format == 'plain':
                docs = [{'text': form_data.read().decode('utf8'), 'file': form_data.name} for form_data in request.FILES.getlist('file')]
                Document.objects.bulk_create([
                    Document(text=doc['text'], file=doc['file'], dataset=dataset)
                    for doc in docs if doc['text'].strip()
                ])



            return HttpResponseRedirect(reverse('dataset_docs', args=[dataset.id]))
        except Exception as e:
            print(e)
            return render(request, 'dataset/upload.html', {"error": str(e), "view": self})

class DownloadView(LoginRequiredMixin, TemplateView):
    template_name = 'dataset/download.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        dataset = get_object_or_404(Dataset, pk=kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['section'] = dataset.name
        context['projects'] = dataset.projects.all()
        return context

    def post(self, request, *args, **kwargs):
        dataset = get_object_or_404(Dataset, pk=kwargs.get('pk'))
        filename = 'corpus_'+dataset.name+'_'+datetime.datetime.today().strftime('%Y%m%d')

        import_format = request.POST['format']
        import_projects = request.POST.getlist('projects')
        annset = Annotation.objects.filter(project__id__in=import_projects, document__dataset=dataset)

        import itertools
        data = sorted(annset, key=lambda x:x.project_id)
        projectset = {key: list(group) for key, group in itertools.groupby(data, key=lambda x:x.project)}

        docset = Document.objects.filter(id__in=set(annset.values_list('document', flat=True)))

        response = self.get_json(filename, projectset, docset)
        return response
        
    def get_json(self, filename, projectset, docset):
        response = HttpResponse(content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="{}.json"'.format(filename)

        docs = [{'doc_id': doc.id, 'file': doc.file, 'dataset': doc.dataset.name, 'text': doc.text} for doc in docset]
        projects = []

        for project, anns in projectset.items():
            projects.append({
                    'name': project.name,
                    'description': project.description,
                    'split_pattern': project.split_pattern,
                    'split_type': project.split_type,
                    'project_type': project.project_type,
                    'annotations': [{'label':ann.label.text, 'doc_id':ann.document.id, 'start': ann.start, 'end': ann.end} for ann in anns]
                })
        
        # dump = json.dumps({'projects': projects, 'docs': docs}, ensure_ascii=False, indent=4)
        dump = json.dumps({'projects': projects, 'docs': docs}, ensure_ascii=False, indent=None, separators=(',', ':'))
        response.write(dump)
        print('dump done')
        return response