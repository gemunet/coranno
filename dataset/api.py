from rest_framework import serializers
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Dataset, Document
from project.models import Project

class DatasetSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    documents_count = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = ('id', 'name', 'description', 'user', 'created_at', 'documents_count', 'updated_at')
        # depth = 1
        # read_only_fields = ('user',)
        # extra_kwargs = {"user": {"required": False, "read_only": True}}

    def get_documents_count(self, obj):
        return obj.documents.count()

    def get_updated_at(self, obj):
        documents = obj.documents.all()
        if(documents):
            return documents.latest('created_at').created_at
        return None

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('dataset', 'text', 'file')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description')


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = (IsAuthenticated,)
    
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated,)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)