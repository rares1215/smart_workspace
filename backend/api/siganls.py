from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from .models import DocumentUpload
from .utils.analyze_text_with_llm import analyze_text
from .utils.extract_text_from_pdf import extract_text