import pytest

pytestmark = pytest.mark.django_db


class TestTodolistHierarchyEndpoints:
    """Test `todolist/hierarchy` API endpoints"""
    endpoint = '/api/todolist/hierarchy/'

    def test_list(self, api_client, hierarchy):
        """Test list method of hierarchy API endpoint"""
        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(response.data) == 2
        assert len(response.data[0].get("children")) == len(hierarchy.children)
        assert response.data[0].get("children")[0].get("name") == hierarchy.children[0].name

    def test_retrieve(self, api_client, hierarchy):
        """
        Test retrieve method of hierarchy API endpoint. Here I take one of subtask to check if it's hierarchy
        retrieves correctly.
        """
        task = hierarchy.children[0]
        response = api_client().get(
            f"{self.endpoint}{task.id}/"
        )

        assert response.status_code == 200
        assert len(response.data.get("children")) == len(task.children)
        assert response.data.get("children")[0].get("name") == task.children[0].name
