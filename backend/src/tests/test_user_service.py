from django.contrib.auth.models import User
from django.test import TestCase
from src.models.custom_user import (
    CustomUser,
    CustomUserSerializer,
    UserSerializer,
)
from src.services.custom_user_service import create_custom_user


class CreateCustomUserTestCase(TestCase):
    def setUp(self):
        self.valid_user_data = {
            "username": "testuser",
            "password": "TestPassword123",
            "email": "testuser@example.com",
        }
        self.invalid_data = [
            # sem '.' no email
            {
                "username": "testuser",
                "password": "TestPassword123",
                "email": "testuser@example",
            },
            # sem '@' no email
            {
                "username": "testuser2",
                "password": "TestPassword123",
                "email": "testuserexample.com",
            },
            # username ja existente
            {
                "username": "testuser",
                "password": "TestPassword123",
                "email": "testuser@example.com",
            },
        ]

    def test_create_custom_user_valid_data(self):
        # Teste para usuario valido
        result = create_custom_user(self.valid_user_data)
        # Pega usuario no BD
        user = User.objects.get(username="testuser")
        custom_user = CustomUser.objects.get(user=user)
        # Valida retorno da funcao
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["user"]["email"], "testuser@example.com")
        # Checa se usuario foi salvo corretamente
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("TestPassword123"))
        self.assertEqual(custom_user.user, user)

    def test_create_custom_user_invalid_data(self):
        # Teste para usuario invalido
        create_custom_user(
            self.valid_user_data
        )  # cria usuario com username = 'testuser'
        for data in self.invalid_data:
            with self.assertRaises(Exception):
                create_custom_user(data)
