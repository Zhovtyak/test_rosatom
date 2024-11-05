import pytest
from rest_framework.test import APIClient
from ..models import Organization, Storage, Distance

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def organization():
    return Organization.objects.create(name='Test Organization', max_biowaste=10, max_glass=10, max_plastic=10,
                                       total_biowaste=0, total_glass=0, total_plastic=0)

@pytest.fixture
def storage():
    return Storage.objects.create(name='Test Storage', max_biowaste=100, max_glass=50, max_plastic=20,
                                  current_biowaste=0, current_glass=0, current_plastic=0)


class TestOrganizationViewSet:
    @pytest.mark.django_db
    def test_create_organization(self, api_client):
        data = {'name': 'Test Organization', 'max_biowaste': 10, 'max_glass': 10, 'max_plastic': 10,
                                       'total_biowaste':0, 'total_glass': 0, 'total_plastic': 0}
        response = api_client.post('/api/organizations/', data=data)
        assert response.status_code == 201
        assert response.data['name'] == 'Test Organization'
        assert Organization.objects.count() == 1

    @pytest.mark.django_db
    def test_retrieve_organization(self, organization, api_client):
        response = api_client.get(f'/api/organizations/{organization.pk}/')
        assert response.status_code == 200
        assert response.data['name'] == organization.name

    @pytest.mark.django_db
    def test_update_organization(self, organization, api_client):
        data = {'name': 'Updated Name', 'max_biowaste': 10, 'max_glass': 10, 'max_plastic': 10,
                                       'total_biowaste':0, 'total_glass': 0, 'total_plastic': 0}
        response = api_client.patch(f'/api/organizations/{organization.pk}/', data=data)
        assert response.status_code == 200

        organization.refresh_from_db()
        assert organization.name == 'Updated Name'

    @pytest.mark.django_db
    def test_delete_organization(self, organization, api_client):
        response = api_client.delete(f'/api/organizations/{organization.pk}/')
        assert response.status_code == 204
        assert not Organization.objects.filter(id=organization.pk).exists()

class TestStorageViewSet:
    @pytest.mark.django_db
    def setup_method(self):
        self.client = APIClient()

    @pytest.mark.django_db
    def test_create_storage(self):
        data = {'name': 'Test Storage', 'max_biowaste': 100, 'max_glass': 50, 'max_plastic': 20,
                                       'current_biowaste':0, 'current_glass': 0, 'current_plastic': 0}
        response = self.client.post('/api/storages/', data=data)
        assert response.status_code == 201
        assert Storage.objects.exists()

    @pytest.mark.django_db
    def test_retrieve_storage(self):
        storage = Storage.objects.create(name='Test Storage')
        response = self.client.get(f'/api/storages/{storage.pk}/')
        assert response.status_code == 200
        assert response.data['name'] == 'Test Storage'

    @pytest.mark.django_db
    def test_update_storage(self, storage, api_client):
        data = {'name': 'Updated Name', 'max_biowaste': 10, 'max_glass': 10, 'max_plastic': 10,
                                       'current_biowaste':0, 'current_glass': 0, 'current_plastic': 0}
        response = api_client.patch(f'/api/storages/{storage.pk}/', data=data)
        assert response.status_code == 200

        storage.refresh_from_db()
        assert storage.name == 'Updated Name'

    @pytest.mark.django_db
    def test_delete_storage(self):
        storage = Storage.objects.create(name='Test Storage')
        response = self.client.delete(f'/api/storages/{storage.pk}/')
        assert response.status_code == 204
        assert not Storage.objects.filter(id=storage.pk).exists()

    @pytest.mark.django_db
    def test_create_storage_with_invalid_data(self):
        data = {'name': '', 'max_biowaste': -10}
        response = self.client.post('/api/storages/', data=data)
        assert response.status_code == 400

class TestDistanceViewSet:
    @pytest.mark.django_db
    def setup_method(self):
        self.client = APIClient()
        self.organization = Organization.objects.create(name='Test Organization')
        self.storage = Storage.objects.create(name='Test Storage')

    @pytest.mark.django_db
    def test_create_distance(self):
        data = {'organization': self.organization.pk, 'storage': self.storage.pk, 'distance': 10}
        response = self.client.post('/api/distances/', data=data)
        assert response.status_code == 201
        assert Distance.objects.count() == 1

    @pytest.mark.django_db
    def test_create_distance_with_invalid_data(self):
        data = {'organization': self.organization.pk, 'storage': self.storage.pk, 'distance': -5}
        response = self.client.post('/api/distances/', data=data)
        assert response.status_code == 400

class TestTransferWasteView:
    @pytest.mark.django_db
    def setup_method(self):
        self.client = APIClient()

    @pytest.mark.django_db
    def test_successful_transfer(self):
        organization = Organization.objects.create(name='Test Org', total_biowaste=100, total_glass=50, total_plastic=30)
        storage = Storage.objects.create(name='Test Storage', max_biowaste=200, max_glass=100, max_plastic=50)
        Distance.objects.create(organization=organization, storage=storage, distance=10)

        response = self.client.post('/api/transfer_waste/', data={'organization_id': organization.id})

        assert response.status_code == 200

        organization.refresh_from_db()
        storage.refresh_from_db()
        assert organization.total_biowaste == 0
        assert organization.total_glass == 0
        assert organization.total_plastic == 0
        assert storage.current_biowaste == 100
        assert storage.current_glass == 50
        assert storage.current_plastic == 30