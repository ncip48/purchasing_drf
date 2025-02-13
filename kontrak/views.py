from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Kontrak, KontrakLampiran
from .serializers import KontrakDetailSerializer, KontrakLampiranSerializer, KontrakSerializer
from core.paginations import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser

class KontrakViewSet(viewsets.ModelViewSet):
    queryset = Kontrak.objects.all()
    serializer_class = KontrakSerializer
    authentication_classes = [JWTAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_permissions(self):
        # Only authenticated users can create, update, or delete
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if not request.user.has_perm('kontrak.view_kontrak'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        kontrak_queryset = self.queryset
        
        paginator = self.pagination_class()
        paginated_kontrak = paginator.paginate_queryset(kontrak_queryset, request)
        
        serializer = self.get_serializer(paginated_kontrak, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        kontrak = get_object_or_404(self.queryset, pk=kwargs['pk'])
        if not request.user.has_perm('kontrak.view_kontrak'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = KontrakDetailSerializer(kontrak)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Check permission for creating a kontrak
        if not request.user.has_perm('kontrak.add_kontrak'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        kontrak = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        # Check permission for updating a kontrak
        if not request.user.has_perm('kontrak.change_kontrak'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(kontrak, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        kontrak = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        # Check permission for deleting a kontrak
        if not request.user.has_perm('kontrak.delete_kontrak'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(kontrak)
        return Response(status=status.HTTP_204_NO_CONTENT)

class KontrakLampiranViewSet(viewsets.ModelViewSet):
    queryset = KontrakLampiran.objects.all()
    serializer_class = KontrakLampiranSerializer
    authentication_classes = [JWTAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]  # For file upload
    pagination_class = PageNumberPagination

    def get_permissions(self):
        # Custom permissions for each action
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated,]
            required_permission = 'add_kontrak_lampiran'
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated,]
            required_permission = 'change_kontrak_lampiran'
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated,]
            required_permission = 'delete_kontrak_lampiran'
        elif self.action == 'list' or self.action == 'retrieve':
            required_permission = 'view_kontrak_lampiran'
        else:
            required_permission = None
        
        # Check custom permission
        if required_permission and not self.request.user.has_perm(f'kontrak.{required_permission}'):
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

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)