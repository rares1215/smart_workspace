from .models import CustomUser,DocumentUpload,ChatMessage
from .serializers import CustomUserSerializer,DocumentUploadSerializer,RagQuery,ChatMessageSerializer,VerifyEmailSerializer
from rest_framework import generics,status,viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .services.rag import rag_answer
from .throttles import DocumentUploadThrotleBurst,DocumentUploadThrotleSustained,QueryPostThrotleBurst,QueryPostThrotleSustained,ResendEmailThrotleBurst,ResendEmailThrotleSustained
from .services.cache_document import get_document_from_cache, set_document_in_cache
from .utils.send_mail import send_verification_email
from .utils.verify_email import create_verification_for_user,verify_code




#### Created the view for Register Page
class RegisterFormViewSet(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save(is_active=False)

        code = create_verification_for_user(user)
        send_verification_email(user.email,code)

        return Response(
            {
                'message':'Account created succesfully, please verify your email',
                'user_id':str(user.id),
                'verification_required':True,
            }
        )
    
### View to send the verification code in the email ###
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self,request,user_id):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

        user = CustomUser.objects.filter(id=user_id).first()
        if not user:
            return Response(
                {"error": "Invalid verification request"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.is_active:
            return Response(
                {"message": "Account already verified"},
                status=status.HTTP_200_OK
            )
        
        is_valid = verify_code(user,code)
        if not is_valid:
            return Response(
                {"error": "Invalid or expired code"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.is_active = True
        user.save(update_fields=['is_active'])

        
        return Response(
            {"message": "Email verified successfully. You can now log in."},
            status=status.HTTP_200_OK
        )

##### view to resend the verification code ####
class ResendVerificationEmail(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ResendEmailThrotleSustained,ResendEmailThrotleBurst]

    def post(self,request,user_id):
        user = CustomUser.objects.filter(id=user_id).first()
        if not user:
            return Response(
                {"error": "Invalid verification request"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.is_active:
            return Response(
                {"message": "Account already verified"},
                status=status.HTTP_200_OK
            )
        
        code = create_verification_for_user(user)
        send_verification_email(user.email,code)

        return Response(
            {"message": "Verification code resent successfully"},
            status=status.HTTP_200_OK
        )

###### the viewset for the Document model
class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]
    throttle_classes = [DocumentUploadThrotleBurst,DocumentUploadThrotleSustained]

    def get_queryset(self):
        return DocumentUpload.objects.filter(user=self.request.user)    
    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)
    def retrieve(self, request, *args, **kwargs):
        document = self.get_object()


        cached_data = get_document_from_cache(document.id)

        if cached_data:
            print("Cached hit!")
            return Response(cached_data)


        serializer = self.get_serializer(document)

        set_document_in_cache(document.id,serializer.data)

        return Response(serializer.data)

#### creating the RAG response end-point
class RAGChatView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [QueryPostThrotleSustained,QueryPostThrotleBurst]

    def post(self, request, document_id):
        # 1. Validate document ownership
        doc = DocumentUpload.objects.filter(id=document_id, user=request.user).first()
        if not doc:
            return Response({"error": "Document not found or not yours."}, status=404)

        # 2. Validate input
        serializer = RagQuery(data=request.data)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data["query"]

        # 3. Generate answer
        result = rag_answer(
            document_id=document_id,
            user=request.user,
            query=query
        )

        # 4. Return full result (clean, no nesting)
        return Response({"answer": result["answer"]}, status=200)

class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, document_id):
        messages = ChatMessage.objects.filter(
            user=request.user,
            document_id=document_id
        ).order_by("created_at")

        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, document_id):
        ChatMessage.objects.filter(
            user=request.user,
            document_id=document_id
        ).delete()

        return Response({"status": "Chat cleared"}, status=status.HTTP_204_NO_CONTENT)

