import pytest


@pytest.fixture(scope='module')
def base_url():
    """Фикстура для базового URL микросервиса."""
    return 'https://reqres.in/'
    #return 'http://localhost:8002'