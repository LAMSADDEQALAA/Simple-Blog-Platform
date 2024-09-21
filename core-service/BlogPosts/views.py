from rest_framework import viewsets, permissions
from .models import BlogPost
from .serializers import BlogPostSerializer,BlogPostCreateUpdateSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BlogPostCreateUpdateSerializer

        return BlogPostSerializer 
