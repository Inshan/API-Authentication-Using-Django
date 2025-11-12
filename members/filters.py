import django_filters
from .models import Member


class MemberFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    role = django_filters.CharFilter(lookup_expr="icontains")
    bio = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Member
        fields = ["name", "role", "bio"]
