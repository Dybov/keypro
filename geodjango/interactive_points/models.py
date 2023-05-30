"""
Module: interactive_points.models

This module contains the models for the interactive_points app
"""
from django.contrib.gis.db import models
from django.contrib.auth import models as auth_models


class Point(models.Model):
    """Database model for interactive Points on the map"""
    location = models.PointField()

    created_by = models.ForeignKey(
        auth_models.User,
        related_name="created_by_user",
        on_delete=models.CASCADE,
    )
    owned_by = models.ForeignKey(
        auth_models.User,
        related_name="owned_by_user",
        on_delete=models.CASCADE,
    )
