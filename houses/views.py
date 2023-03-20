from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import House
from .serializers import HouseSerializer
from stay_concious_api.permissions import IsOwnerOrReadOnly


class HouseList(APIView):
    serialzer_class = HouseSerializer()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

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


class HouseDetail(APIView):
    permmission_class = [IsOwnerOrReadOnly]
    serializer_class = HouseSerializer

    def get_object(self, pk):
        try:
            house = House.objects.get(pk=pk)
            self.check_object_permissions(self.req, house)
            return house
        except House.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        house = self.get_object(pk)
        serialzer = HouseSerializer(
            house, context={'request': request}
        )
        return Response(serialzer.data)

    def put(self, request, pk):
        house = self.get_object(pk)
        serializer = HouseSerializer(
            house, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        house = self.get_object(pk)
        house.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
