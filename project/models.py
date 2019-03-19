import string
from django.db import models
from django.contrib.auth.models import User
from dataset.models import Dataset, Document

class Project(models.Model):
    DOCUMENT_CLASSIFICATION = 'DocumentClassification'
    SEQUENCE_LABELING = 'SequenceLabeling'
    Seq2seq = 'Seq2seq'

    PROJECT_CHOICES = (
        (DOCUMENT_CLASSIFICATION, 'document classification'),
        (SEQUENCE_LABELING, 'sequence labeling'),
        # (Seq2seq, 'sequence to sequence'),
    )

    SPLIT_CHOICES_SPLIT = 'split'
    SPLIT_CHOICES_MATCH = 'match'

    SPLIT_CHOICES = (
        (SPLIT_CHOICES_SPLIT, 'split'),
        (SPLIT_CHOICES_MATCH, 'match'),
    )

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    split_pattern = models.CharField(max_length=255, blank=True, help_text='(optional) regex pattern to parse document in sentences.')
    split_type = models.CharField(max_length=30, choices=SPLIT_CHOICES, default=SPLIT_CHOICES_SPLIT)
    datasets = models.ManyToManyField(Dataset, related_name='projects')
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project_type = models.CharField(max_length=30, choices=PROJECT_CHOICES)
    filter_annotation_ids = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = ('name',)

    def is_type_of(self, project_type):
        return project_type == self.project_type

    def get_progress(self):
        total = Document.objects.filter(dataset__in=self.datasets.all()).count()
        current = self.annotations.values('document').annotate(models.Count('document')).count()
        return {'total': total, 'current': current}

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)

    def get_template_name(self):
        if self.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            template_name = 'annotation/document_classification.html'
        elif self.is_type_of(Project.SEQUENCE_LABELING):
            template_name = 'annotation/sequence_labeling.html'
        elif self.is_type_of(Project.Seq2seq):
            template_name = 'annotation/seq2seq.html'
        else:
            raise ValueError('Template does not exist')

        return template_name

    def get_document_serializer(self):
        from .api import DocumentAnnotationSerializer
        if self.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            return DocumentAnnotationSerializer
        elif self.is_type_of(Project.SEQUENCE_LABELING):
            return DocumentAnnotationSerializer
        # elif self.is_type_of(Project.Seq2seq):
        #     return Seq2seqDocumentSerializer
        else:
            raise ValueError('Invalid project_type')

    def get_documents(self, is_null=True, filter_annotations=None):
        if filter_annotations:
            from django.db.models import Q
            docs = Document.objects.filter(Q(dataset__in=self.datasets.all()) & Q(annotations__label__in=filter_annotations.split(','))).distinct()
        else:
            docs = Document.objects.filter(dataset__in=self.datasets.all())

        if self.is_type_of(Project.DOCUMENT_CLASSIFICATION) or self.is_type_of(Project.SEQUENCE_LABELING):
            if is_null:
                docs = docs.exclude(pk__in=self.annotations.values_list('document', flat=True))
            else:
                docs = docs.filter(pk__in=self.annotations.values_list('document', flat=True))
        # elif self.is_type_of(Project.Seq2seq):
        #     docs = docs.filter(seq2seq_annotations__isnull=is_null)
        else:
            raise ValueError('Invalid project_type')

        return docs

class Label(models.Model):
    KEY_CHOICES = ((u, c) for u, c in zip(string.ascii_lowercase, string.ascii_lowercase))
    COLOR_CHOICES = ()

    text = models.CharField(max_length=100)
    shortcut = models.CharField(max_length=10, choices=KEY_CHOICES)
    project = models.ForeignKey(Project, related_name='labels', on_delete=models.CASCADE)
    background_color = models.CharField(max_length=7, default='#209cee')
    text_color = models.CharField(max_length=7, default='#ffffff')

    def __str__(self):
        return self.text

    class Meta:
        unique_together = (
            ('project', 'text'),
            ('project', 'shortcut')
        )

class Annotation(models.Model):
    project = models.ForeignKey(Project, related_name='annotations', on_delete=models.CASCADE)
    document = models.ForeignKey(Document, related_name='annotations', on_delete=models.CASCADE)
    start = models.IntegerField()
    end = models.IntegerField()
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

    def clean(self):
        if self.start >= self.end:
            raise ValidationError('start is after end')

    class Meta:
        unique_together = ('project', 'document', 'start', 'end', 'label')
