"""
Application Configuration
Environment variables and settings management
"""

import os
from typing import List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings
import toml

class Settings(BaseSettings):
    """
    Application settings with environment variable support
    """
    
    # Application Settings
    APP_NAME: str = "Job Vacancy Insight API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:9100",
        "http://0.0.0.0:9100",
        "http://127.0.0.1:9100"
    ]
    
    # Database Settings (from existing config)
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    
    # Redis Settings
    REDIS_HOST: str = "job_vacancy_insight_redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # Cache Settings
    CACHE_TTL_DEFAULT: int = 1800  # 30 minutes
    CACHE_TTL_SHORT: int = 300     # 5 minutes
    CACHE_TTL_LONG: int = 7200     # 2 hours
    CACHE_TTL_STATIC: int = 86400  # 24 hours
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load database config from existing TOML file
        self._load_database_config()
    
    def _load_database_config(self):
        """Load database configuration from existing config file"""
        try:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                "config",
                "database_config.toml"
            )
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    db_config = toml.load(f)
                
                # Get datawarehouse config (assuming this is what dashboard uses)
                if 'datawarehouse' in db_config:
                    dw_config = db_config['datawarehouse']
                    self.DB_HOST = dw_config.get('host', 'localhost')
                    self.DB_PORT = dw_config.get('port', 5432)
                    self.DB_NAME = dw_config.get('database', 'job_vacancy_insight_datawarehouse')
                    self.DB_USER = dw_config.get('user', 'IsaacLee')
                    self.DB_PASSWORD = dw_config.get('password', 'job_vacancy_insight')
                    
        except Exception as e:
            print(f"Warning: Could not load database config: {e}")
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        if v not in ["development", "staging", "production"]:
            raise ValueError("Environment must be development, staging, or production")
        return v
    
    @property
    def database_url(self) -> str:
        """Generate database URL for SQLAlchemy"""
        if all([self.DB_HOST, self.DB_PORT, self.DB_NAME, self.DB_USER, self.DB_PASSWORD]):
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return "postgresql://user:password@localhost:5432/database"
    
    @property
    def redis_url(self) -> str:
        """Generate Redis URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings()