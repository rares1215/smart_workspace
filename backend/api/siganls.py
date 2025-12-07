from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from .models import DocumentUpload
from .utils.analyze_text_with_llm import analyze_text
from .utils.extract_text_from_pdf import extract_text
import os


@receiver(post_save,sender=DocumentUpload)
def save_text_on_upload(sender,instance,created, **kwargs):
    if not created:
        return
    
    text = extract_text(instance.doc_file.path)
    instance.text = text
    DocumentUpload.objects.filter(id=instance.id).update(text=text)



@receiver(post_delete, sender=DocumentUpload)
def delete_file_after_deleting_model(sender,instance,**kwargs):
    if instance.doc_file and hasattr(instance.doc_file,'path'):
        try:
            file_path = instance.doc_file.path
            if os.path.isfile(file_path):
                print("Removed document from media!")
                os.remove(file_path)
        except:
            print(f"Could not delete document with path:{file_path}")
