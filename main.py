import uvicorn
from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from models.AppStatus import AppStatus
from models.User import User
from fastapi_pagination import Page, add_pagination, paginate
from pydantic import ValidationError
from test_data.users import users_data  # Импортируем данные

app = FastAPI()
add_pagination(app)

users: list[User] = []


# Служебная ручка доступности сервиса
@app.get("/status", status_code=HTTPStatus.OK)
def get_status() -> AppStatus:
    return AppStatus(users=bool(users))


# Получение пользователя по ID
@app.get("/api/user/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int):
    """
    Получает пользователя по ID.
    Возвращает 404, если пользователь не найден.
    """
    if user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="User ID must be greater than 0"
        )

    # Проверяем, есть ли пользователь с таким ID в списке.
    # Перебираем список пользователей и ищем соответствие по ID.
    for user in users:
        if user.id == user_id:  # Вот исправление: user.id (доступ к полю id)
            return user

    # Если пользователь не найден, возвращаем 404.
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="User not found"
    )

# Получение всех пользователей с пагинацией
@app.get("/api/users/", response_model=Page[User], status_code=HTTPStatus.OK)
def get_users() -> Page[User]:
    return paginate(users)


if __name__ == "__main__":
    try:
        # Валидация данных с помощью Pydantic
        for user_data in users_data:
            User.model_validate(user_data)
            users.append(User(**user_data))

        print("Users loaded and validated -> Server started")
    except ValidationError as e:
        print(f"Error: Data validation failed - {e}")

    # Запуск сервера
    uvicorn.run(app, host="localhost", port=8002)