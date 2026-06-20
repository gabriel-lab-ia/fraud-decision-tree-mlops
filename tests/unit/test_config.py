import pytest
from pydantic import ValidationError

from fraud_detection.config import Settings


def test_settings_redacts_api_key():
    settings = Settings(api_key="secret-value", enable_api_key_auth=True)
    assert settings.safe_dict()["api_key"] == "***redacted***"


def test_production_requires_api_key_auth():
    with pytest.raises(ValidationError):
        Settings(app_env="production", enable_api_key_auth=False)


def test_environment_style_cors_parsing():
    settings = Settings(cors_allow_origins="http://a.test,http://b.test")
    assert settings.cors_allow_origins == ["http://a.test", "http://b.test"]
