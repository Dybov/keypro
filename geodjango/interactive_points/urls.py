"""
Module: interactive_points.urls

This module defines the URL patterns and thier namespace for the
interactive_points app.
"""
from django.urls import path

from . import views


app_name = "interactive_points"  # Django way so; pylint: disable=invalid-name
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_point, name="create"),
    path("update/<int:point_id>/", views.update_point, name="update"),
    path("delete/<int:point_id>/", views.delete_point, name="delete"),
]
