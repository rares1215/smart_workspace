from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from .models import DocumentUpload,DocumentEmbedding
from .utils.extract_text_from_pdf import extract_text
from .utils.chunk_text import chunk_text
from .utils.generate_embedings import generate_embedding_for_chunks
import os
from django.core.cache import cache

@receiver(post_save,sender=DocumentUpload)
def save_text_and_embeddings(sender,instance,created, **kwargs):
    if not created:
        return
    
    text = extract_text(instance.doc_file.path)
    instance.text = text
    DocumentUpload.objects.filter(id=instance.id).update(text=text)
    chunks = chunk_text(text)
    vectors = generate_embedding_for_chunks(chunks)

    embeddings_to_make = []
    for index, (chunk, vector) in enumerate(zip(chunks, vectors)):
        if vector is None:
            print(f"Skipping chunk {index}: embedding is None")
            continue

        embeddings_to_make.append(
            DocumentEmbedding(
                document=instance,
                chunk_index=index,
                chunk_text=chunk,
                embedding=vector,
            )
        )

    DocumentEmbedding.objects.bulk_create(embeddings_to_make)

@receiver(post_delete, sender=DocumentUpload)
def delete_file_and_cache_after_deleting_model(sender,instance,**kwargs):
    if instance.doc_file and hasattr(instance.doc_file,'path'):
        try:
            file_path = instance.doc_file.path
            if os.path.isfile(file_path):
                print("Removed document from media!")
                os.remove(file_path)
        except:
            print(f"Could not delete document with path:{file_path}")

    ## invalidating cache after document deletion
    cache.delete(f"document:{instance.id}")
    print(f"[CACHE] Invalidated document:{instance.id}")