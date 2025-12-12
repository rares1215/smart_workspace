import secrets
import string
import hashlib
from datetime import timedelta
from django.utils import timezone
from ..models import EmailVerification

def generate_code(length=6)->str:
    code = string.digits
    return "".join(secrets.choice(code) for i in range(length))

def hash_code(val:str)->str:
    return hashlib.sha256(val.encode('utf-8')).hexdigest()


def create_verification_for_user(user,expire_minutes :int = 10 ):
    
    code = generate_code()
    code_hash = hash_code(code)

    expires_at = timezone.now() + timedelta(minutes=expire_minutes)

    ### only one code per user, if the verification already exists we delete it to make room for new one
    EmailVerification.objects.filter(user=user).delete()


    EmailVerification.objects.create(
        user=user,
        code_hash=code_hash,
        expires_at = expires_at,
        is_used = False,
    )


    return code


def verify_code(user,input_code:str)->bool:
    try:
        verification = EmailVerification.objects.get(user=user)
    except EmailVerification.DoesNotExist:
        return False
    
    if verification.is_used:
        return False
    if timezone.now() > verification.expires_at:
        return False

    input_hash = hash_code(input_code)
    if verification.code_hash != input_hash:
        return False
    
    verification.is_used = True
    verification.save(update_fields=['is_used'])

    return True

