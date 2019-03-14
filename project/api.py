from rest_framework import serializers
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
import re

from dataset.models import Document
from .models import Project, Label, Annotation

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('id', 'text', 'shortcut', 'project', 'background_color', 'text_color')

class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    datasets_count = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    labels = LabelSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'user', 'updated_at', 'split_pattern', 'datasets', 'project_type', 'datasets_count', 'progress', 'labels')

    def get_datasets_count(self, obj):
        return obj.datasets.count()

    def get_progress(self, obj):
        return obj.get_progress()

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ('id', 'label', 'start', 'end')

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = (IsAuthenticated,)

class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = (IsAuthenticated,)

class DocumentAnnotationSerializer(serializers.ModelSerializer):
    annotations = serializers.SerializerMethodField()
    sentences = serializers.SerializerMethodField()

    def get_annotations(self, instance):
        request = self.context.get('request')
        if request:
            project = get_object_or_404(Project, pk=self.context.get('view').kwargs['pk'])

            annotations = project.annotations.filter(document=instance)
            serializer = AnnotationSerializer(annotations, many=True)
            return serializer.data

    def get_sentences(self, obj):
        project = get_object_or_404(Project, pk=self.context.get('view').kwargs['pk'])
        sentences = self.split_text(obj.text, project.split_pattern)
        return [s for s in sentences if s['text']]

    class Meta:
        model = Document
        fields = ('id', 'text', 'sentences', 'file', 'annotations')

    # separa el texto segun una expresion regular
    def split_text(self, text, pattern):
        spans = []

        start = 0
        if pattern:
            it = re.finditer(pattern, text)
            for m in it:
                t = text[start: m.start()]
                spans.append({'text': t, 'start': start, 'end': m.start()})
                start = m.end()
        t = text[start:]
        spans.append({'text': t, 'start': start, 'end': start+len(t)})
        
        return spans

class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('text', )
    page_size = 5
    default_limit = 5
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        self.serializer_class = project.get_document_serializer()

        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])

        annotations = self.request.query_params.get('annotations')
        if annotations:
            from django.db.models import Q
            queryset = self.queryset.filter(Q(dataset__in=project.datasets.all()) & Q(annotations__label__in=annotations.split(','))).distinct() 
        else:
            queryset = self.queryset.filter(dataset__in=project.datasets.all()).distinct()
        
        if not self.request.query_params.get('is_checked'):
            return queryset
        
        is_null = self.request.query_params.get('is_checked') == 'true'
        queryset = project.get_documents(is_null).distinct()

        return queryset

class AnnotationList(generics.ListCreateAPIView):
    pagination_class = None
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        # project = get_object_or_404(Project, pk=self.kwargs['pk'])
        self.serializer_class = AnnotationSerializer

        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        document = Document.objects.get(id=self.kwargs['doc_id'])
        self.queryset = project.annotations.filter(document=document)

        return self.queryset

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        doc = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        serializer.save(project=project, document=doc)

class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        # project = get_object_or_404(Project, pk=self.kwargs['pk'])
        self.serializer_class = AnnotationSerializer

        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        document = Document.objects.get(id=self.kwargs['doc_id'])
        self.queryset = project.annotations.filter(document=document)

        return self.queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['annotation_id'])
        self.check_object_permissions(self.request, obj)

        return obj