from django.core.cache import cache


def get_document_from_cache(document_id):
    key = f"document:{document_id}"
    try:
        return cache.get(key) 
    except ValueError:
        print("Invalid Key")

def set_document_in_cache(document_id,data,exp_time = 60*60*48):
    key = f"document:{document_id}"
    cache.set(key,data,exp_time)