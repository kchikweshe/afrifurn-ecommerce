from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AfriFurn Product Service"
    admin_email: str
    database_url: str
    secret_key: str
    allowed_hosts: list = ["*"]
    debug: bool = False

    class Config:
        env_file = ".env"