"""
Module: interactive_points.admin

This module registers the interactive_points models in the Django admin site.
"""

from django.contrib import admin
from django.contrib.gis import admin as gis_admin

from .models import Point


@admin.register(Point)
class PointAdmin(gis_admin.GISModelAdmin):
    """
    Admin class for the Point model.

    :ivar list_display: The fields to be displayed in the admin list view.
    :vartype list_display: tuple
    """
    list_display = ('location', 'owned_by')
    gis_widget_kwargs = {'attrs': {
        'default_lon': 29.76316,
        'default_lat': 62.60118,
    }}
