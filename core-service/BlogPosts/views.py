from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer, BlogPostCreateUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from .pagination import BlogPostPagination
from .permissions import IsAuthorOrReadOnly 
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated,IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']
    pagination_class = BlogPostPagination

    CACHE_TIMEOUT = 60 * 15  # Cache for 15 minutes

    @method_decorator(cache_page(CACHE_TIMEOUT))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        self.invalidate_cache()

    def perform_update(self, serializer):
        serializer.save()
        self.invalidate_cache()
    
    def perform_destroy(self, instance):
        instance.delete()
        self.invalidate_cache()
    
    def invalidate_cache(self):
        cache.clear()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BlogPostCreateUpdateSerializer
        return BlogPostSerializer
