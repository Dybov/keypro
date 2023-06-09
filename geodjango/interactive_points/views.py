"""
Module: interactive_points.views

This module contains the views for the interactive_points app including
index page that returs map and API for CRUD operations on points
"""
import json

from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point as GeosPoint
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Point


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """
    Index page that returns interactive map

    :param request: The HTTP request object
    :type request: django.http.HttpRequest
    :return: The rendered response
    :rtype: django.http.HttpResponse
    """
    points = serializers.serialize("geojson", Point.objects.all())
    user_id = request.user.id
    return render(request, "interactive_points/map.html", context={
        "points": points, "user_id": user_id})


@login_required
@csrf_exempt
def create_point(request: HttpRequest) -> JsonResponse:
    """
    Create a new point with the provided longitude and latitude coordinates.

    :param request: The HTTP request object.
    :type request: HttpRequest

    :returns: A JSON response containing the ID of the created point.
    :rtype: JsonResponse
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    location = validate_point_data(request)
    if isinstance(location, JsonResponse):
        return location

    user = request.user
    point = Point(location=location, owned_by=user, created_by=user)
    point.save()
    return JsonResponse({'id': point.id})


@login_required
@csrf_exempt
def update_point(request: HttpRequest, point_id: int) -> JsonResponse:
    """
    Update the location of a specific point with the provided longitude and
    latitude coordinates.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param point_id: The ID of the point to update.
    :type point_id: int

    :returns: A JSON response indicating the success of the update.
    :rtype: JsonResponse
    """
    if request.method != 'PUT':
        return HttpResponseNotAllowed(['PUT'])

    point = get_point_for_user(point_id, request)
    if isinstance(point, JsonResponse):
        return point

    location = validate_point_data(request)
    if isinstance(location, JsonResponse):
        return location

    point.location = location
    point.save()
    return JsonResponse({'message': 'success'}, status=201)


def validate_point_data(request):
    """
    Validate JSON data in the request body and create a GeosPoint object.

    :param request: The HTTP request object.
    :type request: HttpRequest

    :returns: the GeosPoint object. If validation fails, it returns a
              JsonResponse with an error message.
    :rtype: django.contrib.gis.geos.Point object or JsonResponse
    """
    try:
        data = json.loads(request.body.decode())
    except json.decoder.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    try:
        lng = float(data["longitude"])
        lat = float(data["latitude"])
        result = GeosPoint(lng, lat)
    except (TypeError, ValueError):
        result = JsonResponse(
            {'error': 'Data should be an object with correct '
                      'longitude and latitude'},
            status=400,
        )
    return result


@login_required
@csrf_exempt
def delete_point(request: HttpRequest, point_id: int) -> HttpResponse:
    """
    Delete a point with the specified ID.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param point_id: The ID of the point to be deleted.
    :type point_id: int

    :returns: A JSON response indicating the success or failure of the
              operation.
    :rtype: JsonResponse
    """
    if request.method != 'DELETE':
        return HttpResponseNotAllowed(['DELETE'])

    point = get_point_for_user(point_id, request)
    if isinstance(point, JsonResponse):
        return point
    point.delete()

    return HttpResponse(status=204)


def get_point_for_user(point_id: int, request: HttpRequest):
    """
    Get the point with the specified ID for the authenticated user.

    :param point_id: The ID of the point to retrieve.
    :type point_id: int
    :param request: The HTTP request object.
    :type request: HttpRequest

    :returns: The point object if found and the user is the owner, otherwise
              a JSON response indicating the error.
    :rtype: Point or JsonResponse
    """
    try:
        point = Point.objects.get(id=point_id)
    except Point.DoesNotExist:
        return JsonResponse(
            {'error': 'This Point does not exist'}, status=404)

    if point.owned_by != request.user:
        return JsonResponse(
            {'error': 'Tshis user cannot delete this Point'},
            status=403
        )
    return point
