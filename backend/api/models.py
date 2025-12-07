from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from pgvector.django import VectorField
# Create your models here.

class CustomUser(AbstractUser):
    pass



class DocumentUpload(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    doc_file = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)



class DocumentEmbedding(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    document = models.ForeignKey(DocumentUpload,on_delete=models.CASCADE)
    chunk_index = models.IntegerField()
    chunk_text = models.TextField()
    embedding = VectorField(dimensions=1024)
    created_at = models.DateTimeField(auto_now_add=True)