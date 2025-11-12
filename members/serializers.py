from rest_framework import serializers
from .models import Member


class MemberSerializer(serializers.ModelSerializer):
    """Class for providing MemberSerializer"""

    class Meta:
        model = Member
        fields = "__all__"
