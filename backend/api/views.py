from .models import CustomUser,DocumentUpload
from .serializers import CustomUserSerializer,DocumentUploadSerializer,RagQuery
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
class RAGView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, document_id):
        serializer = RagQuery(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        query = serializer.validated_data["query"]

        result = rag_answer(document_id=document_id, query=query)

        return Response(result, status=status.HTTP_200_OK)