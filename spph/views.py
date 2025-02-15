from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.shortcuts import get_object_or_404
from .models import SPPH, SPPHLampiran, SPPHVendor
from .serializers import SPPHDetailSerializer, SPPHItemsSerializer, SPPHLampiranSerializer, SPPHSerializer, SPPHPostSerializer
from core.paginations import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser

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
        if not request.user.has_perm('spph.view_spph'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        spph_queryset = self.queryset
        
        paginator = self.pagination_class()
        paginated_spph = paginator.paginate_queryset(spph_queryset, request)
        
        serializer = self.get_serializer(paginated_spph, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        spph = get_object_or_404(self.queryset, pk=kwargs['pk'])
        if not request.user.has_perm('spph.view_spph'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = SPPHItemsSerializer(spph)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Check permission for creating an SPPH
        if not request.user.has_perm('spph.add_spph'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        # Extract vendors from request data
        vendors = request.data.pop('vendors', [])
        
        # Create the SPPH instance
        serializer = SPPHPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        spph = serializer.save()
        
        # Create related SPPHVendor entries
        for vendor_id in vendors:
            SPPHVendor.objects.create(spph=spph, vendor_id=vendor_id)
        
        # Return the created SPPH data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        spph = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        # Check permission for updating an SPPH
        if not request.user.has_perm('spph.change_spph'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = SPPHPostSerializer(spph, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        spph = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        # Check permission for deleting an SPPH
        if not request.user.has_perm('spph.delete_spph'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(spph)
        return Response(status=status.HTTP_204_NO_CONTENT)

class SPPHLampiranViewSet(viewsets.ModelViewSet):
    queryset = SPPHLampiran.objects.all()
    serializer_class = SPPHLampiranSerializer
    authentication_classes = [JWTAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]  # For file upload
    pagination_class = PageNumberPagination

    def get_permissions(self):
        # Map actions to required permissions
        permission_map = {
            'create': 'add_spph_lampiran',
            'update': 'change_spph_lampiran',
            'partial_update': 'change_spph_lampiran',
            'destroy': 'delete_spph_lampiran',
            'list': 'view_spph_lampiran',
            'retrieve': 'view_spph_lampiran',
        }
        
        # Check required permission
        required_permission = permission_map.get(self.action)
        if required_permission and not self.request.user.has_perm(f'spph.{required_permission}'):
            self.permission_denied(self.request, message=f'Permission {required_permission} required.')
        
        return super().get_permissions()


    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        paginator = self.pagination_class()
        paginated_lampiran = paginator.paginate_queryset(queryset, request)
        
        serializer = self.get_serializer(paginated_lampiran, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)