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

    def list(self, request, *args, **kwargs):
        cache_key = f'blog_posts_{request.query_params.urlencode()}'
        cached_response = cache.get(cache_key)

        if cached_response:
            print("returned from cache")
            return Response(cached_response)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data).data
            cache.set(cache_key, paginated_response, 60 * 15)
            print("not returned from cache")
            return Response(paginated_response)

        return Response({"detail": "No data available"}, status=204)

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
        cache.delete_pattern('blog_posts_*')

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BlogPostCreateUpdateSerializer
        return BlogPostSerializer
