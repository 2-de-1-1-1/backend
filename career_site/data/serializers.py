from rest_framework import serializers
from .models import *


class LocationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationInfo
        fields = ['address', 'geo_lat', 'geo_alt']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['name']


class WelfareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Welfare
        fields = ['name']


class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = ['name']


class JobPositionMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPositionMapping
        fields = ['id', 'job_id', 'position_id']


class JobTechMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTechMapping
        fields = ['id', 'job_id', 'tech_id']


class CompanyTechMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyTechMapping
        fields = ['id', 'company_id', 'tech_id']


class CompanyWelfareMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyWelfareMapping
        fields = ['id', 'company_id', 'welfare_id']


class CompanySerializer(serializers.ModelSerializer):
    tech_stack = TechStackSerializer(many=True, allow_null=True)
    welfare = WelfareSerializer(many=True, allow_null=True)
    location = LocationInfoSerializer(source='loc_info_id', read_only=True, allow_null=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'num_employees', 'investment', 'revenue', 'homepage', 'tech_stack',
                  'welfare', 'location']
        depth = 1


class JobSerializer(serializers.ModelSerializer):
    # company_info = CompanySerializer(source='company_id', read_only=True)
    tech_stack = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['min_wage', 'max_wage', 'tech_stack', 'position']

    def get_tech_stack(self, obj):
        job_tech_mapping = JobTechMapping.objects.filter(job_id_id=obj.id).select_related('tech_id')
        tech_stack_names = [mapping.tech_id.name for mapping in job_tech_mapping]
        return tech_stack_names

    def get_position(self, obj):
        job_position_mapping = JobPositionMapping.objects.filter(job_id_id=obj.id).select_related('position_id')
        position_names = [mapping.position_id.name for mapping in job_position_mapping]
        return position_names
