from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=100)

class Document(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='datasets', on_delete=models.CASCADE)
    text = models.TextField()
    file_name = models.CharField(max_length=100)
    