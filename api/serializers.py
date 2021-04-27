from rest_framework import serializers
from django.contrib.auth import get_user_model
from plan.models import Plan, City, Pref


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        exclude = (
            'created_at',
            'updated_at',
        )


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name', 'pref']



class PrefSerializer(serializers.ModelSerializer):

    city = serializers.SerializerMethodField()

    class Meta:
        model = Pref
        fields = ['id', 'pref_name', 'pref_code', 'city']

    def get_city(self, obj):
        try:
            city_child = CitySerializer( City.objects.all().filter(pref=Pref.objects.get(id=obj.id ) ),
                                         many=True).data
            return city_child
        except:
            city_child = None
            return city_child


class PrefChildSerializer(serializers.ListSerializer):

    child = PlanSerializer()


class CityChildSerializer( serializers.ListSerializer):
    child = PrefSerializer()