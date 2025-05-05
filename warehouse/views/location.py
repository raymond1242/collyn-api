from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response

from warehouse.models import Location, UserWarehouse
from warehouse.serializers.location import LocationSerializer


class LocationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    authentication_classes = [TokenAuthentication]

    def get_user_company(self):
        user_company = UserWarehouse.objects.get(user=self.request.user)
        return user_company

    def get_queryset(self):
        company = self.get_user_company().company
        return (
            super(LocationViewSet, self)
            .get_queryset()
            .filter(
                company=company,
            )
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
