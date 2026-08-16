import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.DATABASE_URL = os.getenv("DATABASE_URL", "")
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

        self.NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "")
        self.NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "")

        self.R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID", "")
        self.R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY", "")
        self.R2_SECRET_KEY = os.getenv("R2_SECRET_KEY", "")
        self.R2_PUBLIC_DOMAIN = os.getenv("R2_PUBLIC_DOMAIN", "")

    def validate(self) -> None:
        required_settings = {
            "DATABASE_URL": self.DATABASE_URL,
            "OPENROUTER_API_KEY": self.OPENROUTER_API_KEY,
        }

        missing = [name for name, value in required_settings.items() if not value]

        if missing:
            raise RuntimeError("필수 환경변수가 없습니다: " + ", ".join(missing))


settings = Settings()
