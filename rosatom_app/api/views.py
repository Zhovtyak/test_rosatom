from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Organization, Storage, Distance
from .serializers import OrganizationSerializer, StorageSerializer, DistanceSerializer
from django.db.models import Sum

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer


class DistanceViewSet(viewsets.ModelViewSet):
    queryset = Distance.objects.all()
    serializer_class = DistanceSerializer


class TransferWasteView(APIView):
    def post(self, request):
        organization_id = request.data.get('organization_id')

        # Получаем организацию
        try:
            organization = Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            return Response({'error': 'Организация не найдена'}, status=404)

        # Получаем все расстояния до хранилищ от данной организации
        distances = Distance.objects.filter(organization=organization)

        # Создаем словарь для хранения информации о хранилищах
        storages_data = {}
        for distance in distances:
            storage = distance.storage
            storages_data[storage.id] = {
                'distance': distance.distance,
                'available_space': {
                    'biowaste': storage.max_biowaste - storage.current_biowaste,
                    'glass': storage.max_glass - storage.current_glass,
                    'plastic': storage.max_plastic - storage.current_plastic,
                }
            }

        # Фильтруем хранилища, которые могут вместить все отходы
        suitable_storages = []
        for storage_id, data in storages_data.items():
            if (data['available_space']['biowaste'] >= organization.total_biowaste
                and data['available_space']['glass'] >= organization.total_glass
                and data['available_space']['plastic'] >= organization.total_plastic):
                suitable_storages.append((storage_id, data))

        # Сортируем хранилища по расстоянию
        suitable_storages.sort(key=lambda x: x[1]['distance'])

        # Если есть подходящие хранилища, выбираем ближайшее
        if suitable_storages:
            best_storage_id, _ = suitable_storages[0]
            best_storage = Storage.objects.get(pk=best_storage_id)

            # Обновляем количество отходов в организации и хранилище
            best_storage.current_biowaste += organization.total_biowaste
            best_storage.current_glass += organization.total_glass
            best_storage.current_plastic += organization.total_plastic
            best_storage.save()

            # Обнуляем счетчики отходов в организации
            organization.total_biowaste = 0
            organization.total_glass = 0
            organization.total_plastic = 0
            organization.save()

            return Response({'message': 'Отходы успешно перенесены'})
        else:
            return Response({'error': 'Не найдено подходящее хранилище'}, status=404)

