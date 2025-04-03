from typing import List, Tuple
from test_data.users import users_data

class Users:
    users: List[Tuple[int, str]] = [
        (1, "george.bluth@reqres.in"),
        (2, 'janet.weaver@reqres.in')
    ]


class UserPlusOneFor404:
    @staticmethod
    def non_existent_user_id():
        if users_data:
            # Последний элемент списка всегда будет иметь максимальный ID
            last_user = users_data[-1]
            return last_user['id'] + 1
        else:
            return -1
