from rest_framework.throttling import UserRateThrottle


class DocumentUploadThrotleBurst(UserRateThrottle):
    scope = 'document_upload_burst'

class DocumentUploadThrotleSustained(UserRateThrottle):
    scope = 'document_upload_sustained'


class QueryPostThrotleBurst(UserRateThrottle):
    scope = 'query_burst'

class QueryPostThrotleSustained(UserRateThrottle):
    scope = 'query_sustained'

class ResendEmailThrotleBurst(UserRateThrottle):
    scope = 'resend_burst'

class ResendEmailThrotleSustained(UserRateThrottle):
    scope = 'resend_sustained'