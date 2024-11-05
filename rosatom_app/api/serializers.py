from rest_framework import serializers
from .models import Organization, Storage, Distance


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
    
    def validate(self, data):
        for field_name in ['biowaste', 'glass', 'plastic']:
            if data.get(f'total_{field_name}') > data.get(f'max_{field_name}'):
                raise serializers.ValidationError(
                    f"Количество {field_name} превышает максимальное значение"
                )
        return data


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'
    
    def validate(self, data):
        for field_name in ['biowaste', 'glass', 'plastic']:
            if data.get(f'current_{field_name}') > data.get(f'max_{field_name}'):
                raise serializers.ValidationError(
                    f"Количество {field_name} превышает максимальное значение"
                )
        return data


class DistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distance
        fields = '__all__'