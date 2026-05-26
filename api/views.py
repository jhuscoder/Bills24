import logging
from decimal import Decimal
from django.core.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import permissions, generics
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
from drf_spectacular.utils import extend_schema
from .response import error_response, pending_response, success_response

logger = logging.getLogger(__name__)


class API(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]
    @extend_schema(request=None, responses=None, description="API HEALTH CHECK", summary="API HEALTH CHECK")
    def get(self, request, format=None):
        return success_response("API LIVE")