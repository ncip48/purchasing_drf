from django.urls import path
from purchase_request.views import PurchaseRequestItemsView

urlpatterns = [
    path('purchase-requests/<uuid:purchase_request_id>/items', PurchaseRequestItemsView.as_view(), name='purchase-request-items'),
]
