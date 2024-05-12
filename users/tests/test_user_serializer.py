import pytest
from django.contrib.auth import get_user_model

from users.serializers import UserSerializer

User = get_user_model()


@pytest.fixture
def sample_user_data():
    return {
        "username": "test_user",
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
    }


@pytest.mark.django_db
class TestUserSerializer:
    def test_serializer_with_valid_data(self, sample_user_data):
        serializer = UserSerializer(data=sample_user_data)
        assert serializer.is_valid()

    def test_serializer_with_missing_required_fields(self):
        data = {}
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors
        # assert 'email' in serializer.errors

    def test_serializer_with_invalid_email(self, sample_user_data):
        sample_user_data["email"] = "invalid-email"  # Invalid email format
        serializer = UserSerializer(data=sample_user_data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_serializer_create_method(self, sample_user_data):
        serializer = UserSerializer(data=sample_user_data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.id is not None

    def test_serializer_update_method(self, sample_user_data):
        user = User.objects.create(**sample_user_data)
        updated_data = {
            "first_name": "Updated First Name",
            "last_name": "Updated Last Name",
        }
        serializer = UserSerializer(instance=user, data=updated_data, partial=True)
        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.first_name == updated_data["first_name"]
        assert updated_user.last_name == updated_data["last_name"]
