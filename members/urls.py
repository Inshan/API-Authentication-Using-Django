from django.urls import path, include
from .views import *

urlpatterns = [
    # path("", MemberListAPI.as_view(), name="member-list-api"), --Used when not using 'router'
    path("memberinfo/", member_list_template, name="member-list-template"),
    path("token-login/", token_login_view, name="token-login"),
    # path("", api_root_view, name="api_root_view"),
]
