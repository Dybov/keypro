"""
Module: interactive_points.models

This module contains the models for the interactive_points app
"""
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Point(models.Model):
    """Database model for interactive Points on the map"""
    location = models.PointField()

    created_by = models.ForeignKey(
        User,
        related_name="created_by_user",
        on_delete=models.CASCADE,
    )
    owned_by = models.ForeignKey(
        User,
        related_name="owned_by_user",
        on_delete=models.CASCADE,
    )
