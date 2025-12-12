import sys
from unittest.mock import MagicMock


def setup_mocks():
    """Beállítja a mock modulokat a cirkuláris import elkerülésére."""

    # Mock user_service
    if 'app.services.user_service' not in sys.modules:
        mock_user_service = MagicMock()
        mock_user_service.login = MagicMock()
        sys.modules['app.services.user_service'] = mock_user_service


setup_mocks()


# PYTEST config

def pytest_configure(config):
    """Pytest konfiguráció inicializálása."""
    # Marker regisztráció
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )


import pytest


@pytest.fixture(scope="session")
def test_config():
    """Teszt konfiguráció - session szintű."""
    return {
        "test_mode": True,
        "db_url": "sqlite:///:memory:",
    }
