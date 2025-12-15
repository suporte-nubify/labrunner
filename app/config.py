import os
from dataclasses import dataclass
from urllib.parse import quote_plus


@dataclass
class Settings:
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    app_port: int = 8080

    @property
    def database_url(self) -> str:
        quoted_pwd = quote_plus(self.db_password)
        return (
            f"mysql+pymysql://{self.db_user}:{quoted_pwd}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"
        )


def get_settings() -> Settings:
    required = {
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "DB_NAME": os.getenv("DB_NAME"),
    }

    missing = [name for name, value in required.items() if not value]
    if missing:
        raise RuntimeError(
            f"Variáveis de ambiente ausentes: {', '.join(sorted(missing))}"
        )

    return Settings(
        db_user=required["DB_USER"],
        db_password=required["DB_PASSWORD"],
        db_host=required["DB_HOST"],
        db_port=int(required["DB_PORT"]),
        db_name=required["DB_NAME"],
        app_port=int(os.getenv("PORT", "8080")),
    )


