from django.db import models


class Member(models.Model):
    """Model representing an employee info"""

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    profile_file = models.FileField(upload_to="members/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Dundun for string display"""
        return self.name
