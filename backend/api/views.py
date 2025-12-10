from .models import CustomUser,DocumentUpload,ChatMessage
from .serializers import CustomUserSerializer,DocumentUploadSerializer,RagQuery,ChatMessageSerializer
from rest_framework import generics,status,viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .services.rag import rag_answer




#### Created the view for Register Page
class RegisterFormViewSet(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]



###### the viewset for the Document model
class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]

    def get_queryset(self):
        return DocumentUpload.objects.filter(user=self.request.user)    
    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)

#### creating the RAG response end-point
class RAGChatView(APIView):
    permission_classes = [IsAuthenticated]

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
        return Response(result, status=200)

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

