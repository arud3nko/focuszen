import pytest

from model_bakery import baker

from todolist.models import Task


pytestmark = pytest.mark.django_db


class TestTodolistEndpoints:
    """Test `todolist` app API endpoints"""
    endpoint = '/api/todolist/'

    def test_list(self, api_client):
        """Test list method of API endpoint"""
        baker.make(Task, _quantity=3)

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(response.data) == 3

    def test_create(self, api_client, make_task_bakery):
        """Test create method of API endpoint. Here I test if the response contains source data"""
        task, expected_json = make_task_bakery

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 201
        assert expected_json.items() <= response.data.items()

    def test_retrieve(self, api_client, make_task_bakery):
        """Test retrieve method of API endpoint."""
        task, expected_json = make_task_bakery

        _url = f"{self.endpoint}{task.pk}/"

        response = api_client().get(
            _url
        )

        assert response.status_code == 200
        assert expected_json.items() <= response.data.items()

    def test_update(self, api_client, prepare_task_bakery):
        """Test update method of API endpoint"""
        old = baker.make(Task)
        new, expected_json = prepare_task_bakery

        _url = f"{self.endpoint}{old.pk}/"

        response = api_client().put(
            _url,
            expected_json,
            format='json'
        )

        assert response.status_code == 200
        assert expected_json.items() <= response.data.items()

    @pytest.mark.parametrize(
        'field', [
            'name',
            'description',
            'status',
            'planned_effort',
            'actual_effort',
            'performer',
            'parent'
        ]
    )
    def test_partial_update(self, api_client, prepare_task_bakery, field):
        """Test partial update method of API endpoint"""
        old = baker.make(Task)
        new, expected_json = prepare_task_bakery

        _url = f"{self.endpoint}{old.pk}/"

        response = api_client().patch(
            _url,
            {field: expected_json[field]},
            format='json'
        )

        assert response.status_code == 200
        assert expected_json[field] == response.data.get(field)

    def test_delete(self, api_client):
        """Test deletion method of API endpoint"""
        task = baker.make(Task)
        _url = f"{self.endpoint}{task.pk}/"

        response = api_client().delete(_url)

        assert response.status_code == 204
        assert Task.objects.all().count() == 0
