"""
Module: interactive_points.views

This module contains the views for the interactive_points app including
index page that returs map and API for CRUD operations on points
"""
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    """
    Index page that returns interactive map

    :param request: The HTTP request object
    :type request: django.http.HttpRequest
    :return: The rendered response
    :rtype: django.http.HttpResponse
    """
    return render(request, "interactive_points/map.html")
