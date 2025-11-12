# pylint: disable=no-member
import requests
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import Member
from .serializers import MemberSerializer
from django.http import HttpResponse
from django.contrib.auth import login
from rest_framework.permissions import BasePermission

# from rest_framework.permissions import DjangoModelPermissions


class SelectiveCRUDPermission(BasePermission):
    """
    Custom permission that allows selective CRUD access:
      - GET: allowed for any authenticated user
      - POST: allowed only for staff
      - PUT/PATCH: allowed for staff or the object's owner
      - DELETE: disabled for everyone (example)
    """

    def has_permission(self, request, view):
        # Deny if not authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow GET for all authenticated users
        if request.method == "GET":
            return True

        # Allow POST only for staff/admins
        if request.method == "POST":
            return request.user.is_staff

        # Allow PUT/PATCH only for staff or owner check (below)
        if request.method in ["PUT", "PATCH"]:
            return True  # we'll verify owner at object level

        # Block DELETE for everyone
        if request.method == "DELETE":
            return None

        return False

    def has_object_permission(self, request, view, obj):
        # Owner or staff can edit
        if request.method in ["PUT", "PATCH"]:
            return request.user.is_staff or obj.created_by == request.user
        return True


class MemberViewSet(viewsets.ModelViewSet):
    """A ViewSet for viewing, editing, creating, and deleting Member."""

    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, SelectiveCRUDPermission]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    # View Updation for Filtering (The below 3 statements)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name", "role", "bio"]
    search_fields = ["name", "role", "bio"]
    ordering_fields = ["created_at", "name"]


def member_list_template(request):
    """Function for templating"""

    members = Member.objects.all().order_by("-created_at")
    return render(request, "members/member_list.html", {"members": members})


def token_login_view(request):
    context = {}

    if request.method == "POST":
        token_input = request.POST.get("token")

        try:
            token_obj = Token.objects.get(key=token_input)
            user = token_obj.user

            # Log in the user via session
            login(request, user)  # Now browser session is authenticated

            # Redirect to DRF root
            return redirect("/api/")  # User can now access full browsable API

        except Token.DoesNotExist:
            context["error"] = "❌ Invalid token. Please try again."

    return render(request, "members/token_login.html", context)
