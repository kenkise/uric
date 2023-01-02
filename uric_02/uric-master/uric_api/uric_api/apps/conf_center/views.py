from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Environment
from .serializers import EnvironmentModelSerializer


# Create your views here.
class EnvironmentAPIView(ListAPIView, CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Environment.objects.all()
    serializer_class = EnvironmentModelSerializer
