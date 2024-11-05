from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'storages', views.StorageViewSet)
router.register(r'distances', views.DistanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('transfer_waste/', views.TransferWasteView.as_view()),
]