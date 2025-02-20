from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.test import TestCase
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError
from src.models.custom_user_model import CustomUser
from src.services.custom_user_service import (
    create_custom_user,
    delete_custom_user,
    read_custom_user,
    update_custom_user,
)

VALID_USER_INPUT_MOCK = [
    # 8 caracteres
    {
        "username": "testuser",
        "password": "1234abcd",
        "email": "testuser@example.com",
    },
    # 128 caracteres (limite do Django)
    {
        "username": "testuser44",
        "password": "a1B9k3xY7Q5tZ2mNp6R4Lc8Wd0HvXyCzPqMTJrVoKfEhGuAiBvRnTsUwOpLM3X8Y9Q4kZ7J2a6Nd5RmtCqXpHvWyKoVTJ1LfEhGuA0PzRaaaaaaaaaaaaaaaaaaaaaaa",
        "email": "testuser@example.com",
    },
]

INVALID_USER_INPUT_MOCKS = [
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
    # senha com 7 caracteres
    {"username": "testuser2", "password": "123h456", "email": "testeteste@teste.com"},
    # senha com 129 caracteres
    {
        "username": "testuser2",
        "password": "123h456",
        "email": "a1B9k3xY7Q5tZ2mNp6R4Lc8Wd0HvXyCzPqMTJrVoKfEhGuAiBvRnTsUwOpLM3X8Y9Q4kZ7J2a6Nd5RmtCqXpHvWyKoVTJ1LfEhGuA0PzRaaaaaaaaaaaaaaaaaaaaaaaa",
    },
]

VALID_USER_UPDATE_MOCK = [
    # update email/username
    {
        "username": "testuser_updated",
        "email": "testuser@example.com",
    },
    # update username
    {
        "username": "testuser_updated2",
    },
    # update email
    {
        "email": "testuser@example.com",
    },
]

INVALID_USER_UPDATE_MOCKS = [
    # sem '.' no email
    {
        "username": "testuser_updated",
        "email": "testuser@example",
    },
    # sem '@' no email
    {
        "username": "testuser_updated2",
        "email": "testuserexample.com",
    },
    # username ja existente
    {
        "username": "testuser",
        "email": "testuser@example.com",
    },
]


class TestCreateCustomUserService(TestCase):
    def test_create_custom_user_valid_data(self):

        index = 1

        for data in VALID_USER_INPUT_MOCK:
            # Teste para usuario valido

            result = create_custom_user(data)
            # Pega usuario no BD
            user = User.objects.get(username=data["username"])
            custom_user = CustomUser.objects.get(user=user)

            # Valida retorno da funcao
            self.assertEqual(result["id"], index)
            self.assertEqual(result["user"]["email"], data["email"])
            self.assertEqual(user.email, data["email"])
            self.assertTrue(user.check_password(data["password"]))
            self.assertEqual(custom_user.user, user)

            index += 1

    def test_create_custom_user_invalid_data(self):
        # Teste para usuario invalido

        # cria usuario com username = 'testuser' para testar se tem usuario com nome repetido
        create_custom_user(VALID_USER_INPUT_MOCK[0])
        for data in INVALID_USER_INPUT_MOCKS:
            with self.assertRaises(Exception):
                create_custom_user(data)


class ReadUserTestCase(TestCase):
    def setUp(self) -> None:
        create_custom_user(VALID_USER_INPUT_MOCK[1])

    def tearDown(self) -> None:
        if len(User.objects.filter(id=1)):
            User.objects.filter(id=1).delete()

    def test_read_user_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            read_custom_user(0)
        with self.assertRaises(ObjectDoesNotExist):
            read_custom_user(2)

    def test_read_user_successfully(self):
        result = read_custom_user(1)
        assert result["id"] == 1
        assert result["user"]["email"] == VALID_USER_INPUT_MOCK[1]["email"]


class TestDeleteCustomUserService(TestCase):
    def setUp(self) -> None:
        self.user = create_custom_user(VALID_USER_INPUT_MOCK[0])
        self.requesting_user = User.objects.create_user(
            username="admin", password="admin", is_superuser=True
        )

    def tearDown(self) -> None:
        if len(User.objects.filter(id=1)):
            User.objects.filter(id=1).delete()

    def test_custom_user_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            delete_custom_user(0, self.requesting_user)

    def test_custom_user_deleted_successfully(self):
        delete_custom_user(1, self.requesting_user)
        assert len(User.objects.filter(id=1)) == 0

    def test_custom_user_delete_permission_denied(self):
        non_superuser = User.objects.create_user(username="nonadmin", password="nonadmin")
        with self.assertRaises(PermissionDenied):
            delete_custom_user(1, non_superuser)


class TestUpdateCustomUserService(TestCase):
    def setUp(self) -> None:
        self.user = create_custom_user(VALID_USER_INPUT_MOCK[0])
        self.requesting_user = User.objects.create_user(
            username="admin", password="admin", is_superuser=True
        )

    def tearDown(self) -> None:
        if len(User.objects.filter(id=1)):
            User.objects.filter(id=1).delete()

    def test_update_custom_user_valid_data(self):
        user = User.objects.get(username=VALID_USER_INPUT_MOCK[0]["username"])
        custom_user = CustomUser.objects.get(user=user)

        for data in VALID_USER_UPDATE_MOCK:
            result = update_custom_user(data, custom_user.id, self.requesting_user)
            user.refresh_from_db()
            custom_user.refresh_from_db()

            if "username" in data:
                self.assertEqual(user.username, data["username"])
            if "email" in data:
                self.assertEqual(user.email, data["email"])

    def test_update_custom_user_invalid_data(self):
        user = User.objects.get(username=VALID_USER_INPUT_MOCK[0]["username"])
        custom_user = CustomUser.objects.get(user=user)

        for data in INVALID_USER_UPDATE_MOCKS[
            :-1
        ]:  # nao pega o caso do username ja existente
            with self.assertRaises(ValidationError):
                update_custom_user(data, custom_user.id, custom_user.user)

    def test_custom_user_update_permission_denied(self):
        non_superuser = User.objects.create_user(username="nonadmin", password="nonadmin")
        with self.assertRaises(PermissionDenied):
            update_custom_user({"username": "newusername"}, 1, non_superuser)
