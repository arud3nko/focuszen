import pytest

from todolist.serializers import TaskSerializer
from todolist.models import Task

pytestmark = pytest.mark.django_db


class TestTaskSerializer:
    """This class provides tests for `TaskSerializer`"""

    def test_serialize_model(self, make_task_bakery):
        """Test model serialization"""
        task, expected = make_task_bakery

        serialized = TaskSerializer(task)

        assert expected.items() <= serialized.data.items()

    def test_serialize_data(self, prepare_task_bakery):
        """Test data serialization"""
        task, expected = prepare_task_bakery

        serializer = TaskSerializer(data=expected)

        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}

    def test_self_parent(self, make_task_bakery):
        """Test if task cannot be its own parent"""
        task, expected = make_task_bakery
        expected["parent"] = task.pk

        serializer = TaskSerializer(task, data=expected, partial=True)

        assert not serializer.is_valid()
        assert serializer.errors != {}

    @pytest.mark.parametrize("wrong_field", (
            {"status": "none"},
            {"planned_effort": -1},
            {"actual_effort": -1}
    ))
    def test_deserialize_fails(self, wrong_field: dict, prepare_task_bakery):
        task, expected = prepare_task_bakery
        task_fields = [field.name for field in Task._meta.get_fields()]
        invalid_serialized_data = {
                                      k: v for (k, v) in task.__dict__.items() if
                                      k in task_fields and k != "id"
                                  } | wrong_field

        serializer = TaskSerializer(data=invalid_serialized_data)

        assert not serializer.is_valid()
        assert serializer.errors != {}
