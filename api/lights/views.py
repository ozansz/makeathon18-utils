from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from rest_framework.authtoken.models import Token
from rest_framework import generics, status

from lights.models import *
from lights.utils import get_optimal_process_time

__all__ = [
    'TokenView',
    'SensorView',
    'CamView',
    'TimingView',
]

class IEEEAuth(TokenAuthentication):
    keyword = "IEEE-METU"

class TokenView(APIView):
    #permission_classes = (IsAdminUser,)

    def get(self, request, id):
        try:
            node = Node.objects.get(id=id)
        except ObjectDoesNotExist:
            raise NotFound(detail={"error": "node not found"})

        token, created = Token.objects.get_or_create(user=node.user)

        return Response(data={"id": id, "token": token.key})

class SensorView(APIView):
    #permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response(data={"data": request.data})

class CamView(APIView):
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (IEEEAuth,)

    def post(self, request):
        try:
            node = Node.objects.get(id=request.data['id'])
        except ObjectDoesNotExist:
            raise NotFound(detail={"error": "node not found"})

        node.density_records.create(density=float(request.data['density']))

        return Response(status=status.HTTP_200_OK)

class TimingView(APIView):
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (IEEEAuth,)

    def post(self, request):
        try:
            node = Node.objects.get(id=request.data['id'])
        except ObjectDoesNotExist:
            raise NotFound(detail={"error": "node not found"})

        if request.data['stay_or_go'] not in ["stay", "go"]:
            raise ParseError()

        optimal_one = get_optimal_process_time(node, request.data['stay_or_go'])

        return Response(data={"secs": optimal_one})
