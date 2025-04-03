from http import HTTPStatus
import requests
import pytest
from test_data.test_data import *




class TestApi:


    @pytest.mark.parametrize(
        'user_id, expected_email', Users.users
    )
    def test_get_user_id(self, base_url: str, user_id: int, expected_email: str) -> None:
        # Получаем данные о пользователе по его ID
        try:
            response = requests.get(f'{base_url}/api/user/{user_id}')
            assert response.status_code == HTTPStatus.OK, f"Ожидался статус-код 200, получен {response.status_code}"
            user_data = response.json()
        except requests.exceptions.RequestException as e:
            pytest.fail(f'Ошибка при запросе: {e}')

        # Проверяем, что email пользователя соответствует ожидаемому
        assert user_data['email'] == expected_email, (
            f'Неверный email для пользователя с id={user_id}. '
            f'Ожидалось: {expected_email}, получено: {user_data["email"]}'
        )


    # Дополнительный тест для проверки пагинации
    def test_get_users_pagination(self, base_url: str):
        try:
            response = requests.get(f'{base_url}/api/users/')
            assert response.status_code == HTTPStatus.OK, f"Ожидался статус-код 200, получен {response.status_code}"
            users_data = response.json()
        except requests.exceptions.RequestException as e:
            pytest.fail(f'Ошибка при запросе: {e}')

        # Проверяем, что данные возвращаются в правильном формате
        assert 'items' in users_data, "Ключ 'items' отсутствует в ответе"
        assert isinstance(users_data['items'], list), "Данные пользователей должны быть списком"

        # Проверяем, что количество пользователей соответствует ожидаемому
        assert len(users_data['items']) > 0, "Список пользователей пуст"


    def test_get_non_existent_user(self, base_url: str):

        over_user = UserPlusOneFor404.users_plus_one_from_list_users()
        print(over_user)
        response = requests.get(f"{base_url}/api/user/{over_user}")
        r = response.json()
        assert response.status_code == 404 and r == {'detail': 'User not found'}