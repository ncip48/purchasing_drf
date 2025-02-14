from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.shortcuts import get_object_or_404
from .models import SPPH
from .serializers import SPPHSerializer, SPPHPostSerializer
from core.paginations import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

class SPPHViewSet(viewsets.ModelViewSet):
    queryset = SPPH.objects.all()
    serializer_class = SPPHSerializer  # Assuming you have a serializer for SPPH
    authentication_classes = [JWTAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_permissions(self):
        # Only authenticated users can create, update, or delete
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if not request.user.has_perm('kontrak.view_spph'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        spph_queryset = self.queryset
        
        paginator = self.pagination_class()
        paginated_spph = paginator.paginate_queryset(spph_queryset, request)
        
        serializer = self.get_serializer(paginated_spph, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        spph = get_object_or_404(self.queryset, pk=kwargs['pk'])
        if not request.user.has_perm('kontrak.view_spph'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = SPPHSerializer(spph)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Check permission for creating an SPPH
        if not request.user.has_perm('kontrak.add_spph'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = SPPHPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        spph = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        # Check permission for updating an SPPH
        if not request.user.has_perm('kontrak.change_spph'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = SPPHPostSerializer(spph, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        spph = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        # Check permission for deleting an SPPH
        if not request.user.has_perm('kontrak.delete_spph'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(spph)
        return Response(status=status.HTTP_204_NO_CONTENT)
