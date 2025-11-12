from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# for CRUD Operation
router = DefaultRouter()
router.register(r"members", MemberViewSet)

urlpatterns = [
    # path("", MemberListAPI.as_view(), name="member-list-api"), --Used when not using 'router'
    path("", include(router.urls)),
]
