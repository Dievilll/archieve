# from pydantic_settings import BaseSettings

tags_metadata = [
    {
        'name': 'records',
        'description': 'Авторизация и регистрация',
    },
    {
        'name': 'db',
        'description': 'Работа с операциями',
    },
    {
        'name': 'operations',
        'description': 'Импорт и экспорт отчетов',
    },
]


# # Параметры конфигурации которыми можно управлять из вне
# class Settings(BaseSettings):
#     server_host: str = '127.0.0.1'
#     server_port: int = 8000
#     database_url: str = 'sqlite:///./database.sqlite3'

#     jwt_secret: str
#     jwt_algorithm: str = 'HS256'
#     jwt_expiration: int = 3600


# settings = Settings(
#     _env_file='.env',
#     _env_file_encoding='utf8',
# )ss
