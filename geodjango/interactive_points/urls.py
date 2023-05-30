"""
Module: interactive_points.urls

This module defines the URL patterns and thier namespace for the interactive_points app.
"""
from django.urls import path

from . import views


app_name = "interactive_points"  # Django way so; pylint: disable=invalid-name
urlpatterns = [
    path("", views.index, name="index"),
]
