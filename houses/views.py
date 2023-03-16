from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import House
from .serializers import HouseSerializer


class HouseList(APIView):
    serialzer_class = HouseSerializer()

    def get(self, request):
        houses = House.objects.all()
        serialzer = HouseSerializer(
            houses, many=True, context={'request': request}
        )
        return Response(serialzer.data)

    def post(self, request):
        serialzer = HouseSerializer(
            data=request.data, context={'request': request}
        )
        if serialzer.is_valid():
            serialzer.save(owner=request.user)
            return Response(serialzer.data, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
