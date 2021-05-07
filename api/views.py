from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework import status, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializers import PlanSerializer, PrefSerializer
from plan.models import Plan, Pref


class PlanViewSet(ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class PrefFilters(filters.FilterSet):

    class Meta:
        model = Pref
        fields = ['pref_name', 'pref_code']


class PrefList(views.APIView):

    def get(self, request, *args, **kwargs):
        filterset = PrefFilters(request.query_params, Pref.objects.all())
        if not filterset.is_valid():
            raise ValidationError(filterset.errors)
        serializer = PrefSerializer(instance=filterset.qs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status=status.HTTP_201_CREATED )
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )



