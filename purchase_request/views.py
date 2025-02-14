# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from core.paginations import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.shortcuts import get_object_or_404
from .models import PurchaseRequest, PurchaseRequestDetail
from .serializers import PurchaseRequestDetailPostSerializer, PurchaseRequestItemsSerializer, PurchaseRequestPostSerializer, PurchaseRequestSerializer, PurchaseRequestDetailSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView


class PurchaseRequestViewSet(viewsets.ModelViewSet):
    queryset = PurchaseRequest.objects.all()
    serializer_class = PurchaseRequestSerializer
    authentication_classes = [JWTAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_permissions(self):
        # Only authenticated users can create, update, or delete
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if not request.user.has_perm('purchaserequest.view_purchase_request'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        purchase_request_queryset = self.queryset
        
        paginator = self.pagination_class()
        paginated_purchase_requests = paginator.paginate_queryset(purchase_request_queryset, request)
        
        serializer = self.get_serializer(paginated_purchase_requests, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        purchase_request = get_object_or_404(self.queryset, pk=kwargs['pk'])
        if not request.user.has_perm('purchaserequest.view_purchase_request'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = PurchaseRequestItemsSerializer(purchase_request)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Check permission for creating a purchase request
        if not request.user.has_perm('purchaserequest.add_purchase_request'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = PurchaseRequestPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        purchase_request = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        # Check permission for updating a purchase request
        if not request.user.has_perm('purchaserequest.change_purchase_request'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = PurchaseRequestPostSerializer(purchase_request, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        purchase_request = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        # Check permission for deleting a purchase request
        if not request.user.has_perm('purchaserequest.delete_purchase_request'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(purchase_request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseRequestDetailViewSet(viewsets.ModelViewSet):
    queryset = PurchaseRequestDetail.objects.all()
    serializer_class = PurchaseRequestDetailSerializer
    authentication_classes = [JWTAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_permissions(self):
        # Only authenticated users can create, update, or delete
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if not request.user.has_perm('purchaserequest.view_purchase_request_detail'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        purchase_request_detail_queryset = self.queryset
        
        paginator = self.pagination_class()
        paginated_purchase_request_details = paginator.paginate_queryset(purchase_request_detail_queryset, request)
        
        serializer = self.get_serializer(paginated_purchase_request_details, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        purchase_request_detail = get_object_or_404(self.queryset, pk=kwargs['pk'])
        if not request.user.has_perm('purchaserequest.view_purchase_request_detail'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(purchase_request_detail)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Check permission for creating a purchase request detail
        if not request.user.has_perm('purchaserequest.add_purchase_request_detail'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = PurchaseRequestDetailPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        purchase_request_detail = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        # Check permission for updating a purchase request detail
        if not request.user.has_perm('purchaserequest.change_purchase_request_detail'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = PurchaseRequestDetailPostSerializer(purchase_request_detail, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        purchase_request_detail = get_object_or_404(self.queryset, pk=kwargs['pk'])
        
        # Check permission for deleting a purchase request detail
        if not request.user.has_perm('purchaserequest.delete_purchase_request_detail'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(purchase_request_detail)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseRequestItemsView(APIView):
    def get(self, request, purchase_request_id):
        # Get the PurchaseRequest object or return 404
        purchase_request = get_object_or_404(PurchaseRequest, id=purchase_request_id)
        
        # Get related PurchaseRequestDetail items
        items = PurchaseRequestDetail.objects.filter(purchase_request=purchase_request)
        
        # Serialize the items
        serializer = PurchaseRequestDetailSerializer(items, many=True)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)