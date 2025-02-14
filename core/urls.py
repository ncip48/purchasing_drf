"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from kontrak.views import KontrakLampiranViewSet, KontrakViewSet
from purchase_request.views import PurchaseRequestDetailViewSet, PurchaseRequestViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from spph.views import SPPHLampiranViewSet, SPPHViewSet
from vendor.views import VendorViewSet

router = DefaultRouter()
router.register(r'kontrak', KontrakViewSet, basename='kontrak')
router.register(r'kontrak-lampiran', KontrakLampiranViewSet, basename='kontrak-lampiran')
router.register(r'vendor', VendorViewSet, basename='vendor')
router.register(r'purchase-requests', PurchaseRequestViewSet, basename="purchase-request")
router.register(r'purchase-request-details', PurchaseRequestDetailViewSet, basename="purchae-request-detail")
router.register(r'spphs', SPPHViewSet, basename="spph")
router.register(r'spph-lampirans', SPPHLampiranViewSet, basename="spph-lampiran")

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/', include("users.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api-auth/", include("rest_framework.urls")),  
    path('admin/', admin.site.urls),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)