# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from core.paginations import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.shortcuts import get_object_or_404
from .models import Vendor
from .serializers import VendorSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [JWTAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_permissions(self):
        # Only authenticated users can create, update, or delete
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if not request.user.has_perm('vendor.view_vendor'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        vendor_queryset = self.queryset
        
        paginator = self.pagination_class()
        paginated_vendors = paginator.paginate_queryset(vendor_queryset, request)
        
        serializer = self.get_serializer(paginated_vendors, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        vendor = get_object_or_404(self.queryset, pk=kwargs['pk'])
        if not request.user.has_perm('vendor.view_vendor'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(vendor)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Check permission for creating a vendor
        if not request.user.has_perm('vendor.add_vendor'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        vendor = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        # Check permission for updating a vendor
        if not request.user.has_perm('vendor.change_vendor'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(vendor, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        vendor = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        # Check permission for deleting a vendor
        if not request.user.has_perm('vendor.delete_vendor'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(vendor)
        return Response(status=status.HTTP_204_NO_CONTENT)
