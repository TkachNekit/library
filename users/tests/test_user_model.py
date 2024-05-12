import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_user_creation(self):
        user = User.objects.create(
            username="test_user", email="test@example.com", phone_number="1234567890"
        )
        assert user.username == "test_user"
        assert user.email == "test@example.com"
        assert user.phone_number == "1234567890"
        assert not user.is_verified_email
        assert user.date_of_birth is None

    def test_invalid_phone_number(self):
        with pytest.raises(ValidationError):
            user = User.objects.create(
                username="test_user", email="test@example.com", phone_number="invalid"
            )
            user.full_clean()

    # def test_image_upload(self):
    #     # Test uploading an image and verify it's stored correctly
    #     user = User.objects.create(username='test_user', email='test@example.com', phone_number='1234567890')
    #     with open('path/to/test_image.jpg', 'rb') as img_file:
    #         user.image.save('test_image.jpg', img_file)
    #     assert user.image.url.startswith('users_image/')
