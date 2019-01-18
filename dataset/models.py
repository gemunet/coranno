from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name',)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)

class Document(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='documents', on_delete=models.CASCADE)
    text = models.TextField()
    file = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    