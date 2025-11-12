# pylint: disable=no-member
import requests
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login
from .models import Member
from .serializers import MemberSerializer

# from rest_framework.permissions import DjangoModelPermissions


class MemberViewSet(viewsets.ModelViewSet):
    """A ViewSet for viewing, editing, creating, and deleting Member."""

    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

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

        # Check if token exists in DB
        try:
            token_obj = Token.objects.get(key=token_input)
            user = token_obj.user
            context["success"] = f"Access granted for user: {user.username}"
            return render(request, "members/member_list.html", context)

        except Token.DoesNotExist:
            context["error"] = "Invalid token. Please try again."

    return render(request, "members/token_login.html", context)


def api_view(request):
    token = request.session.get("api_token")
    if not token:
        return redirect("token-login")

    api_url = request.build_absolute_uri("/api/members/")
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(api_url, headers=headers)

    return HttpResponse(
        response.content,
        status=response.status_code,
        content_type=response.headers.get("content-type"),
    )
