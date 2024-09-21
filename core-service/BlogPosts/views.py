from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer, BlogPostCreateUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from .pagination import BlogPostPagination

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']
    pagination_class = BlogPostPagination

    def list(self, request, *args, **kwargs):
        cache_key = f'blog_posts_{request.query_params.urlencode()}'
        posts = cache.get(cache_key)

        if not posts:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                posts = serializer.data
                cache.set(cache_key, posts, 60 * 15)
                return self.get_paginated_response(posts)

        return Response(posts)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BlogPostCreateUpdateSerializer
        return BlogPostSerializer
