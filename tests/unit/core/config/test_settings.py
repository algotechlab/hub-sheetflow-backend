from src.core.config.settings import Settings, get_settings


def test_settings_custom_env_values(mock_env, clear_cache):
    # Arrange: Seta env vars custom
    mock_env({
        'ENVIRONMENT': 'production',
        'APP_NAME': 'custom-app',
        'DEBUG': 'true',
        'SQLALCHEMY_DATABASE_URI': 'custom-uri',
        'BACKEND_CORS_ORIGINS': 'http://localhost:3000,http://localhost:4200',
    })

    # Act: Instancia settings
    settings = Settings()

    # Assert: Verifica valores custom
    assert settings.APP_NAME == 'custom-app'
    assert settings.DEBUG is True
    assert settings.SQLALCHEMY_DATABASE_URI == 'custom-uri'
    assert settings.BACKEND_CORS_ORIGINS == [
        'http://localhost:3000',
        'http://localhost:4200',
    ]


def test_cors_origins_validator_string(mock_env, clear_cache):
    # Arrange: CORS como string separada por vírgula
    mock_env({'BACKEND_CORS_ORIGINS': 'http://test1.com, http://test2.com'})

    # Act
    settings = Settings()

    # Assert: Split correto
    assert settings.BACKEND_CORS_ORIGINS == ['http://test1.com', 'http://test2.com']


def test_cors_origins_validator_list(mock_env, clear_cache):
    settings = Settings(BACKEND_CORS_ORIGINS=['http://test1.com', 'http://test2.com'])

    assert settings.BACKEND_CORS_ORIGINS == ['http://test1.com', 'http://test2.com']


def test_get_settings_singleton(clear_cache):
    # Act: Chama duas vezes
    settings1 = get_settings()
    settings2 = get_settings()

    # Assert: Mesma instância (singleton via cache)
    assert settings1 is settings2


def test_get_settings_different_env_changes(mock_env, clear_cache):
    # Arrange: Primeiro com um env
    mock_env({'APP_NAME': 'app1'})
    settings1 = get_settings()

    # Muda env (mas como cache, não muda; pra testar mudança, clear cache)
    get_settings.cache_clear()
    mock_env({'APP_NAME': 'app2'})
    settings2 = get_settings()

    # Assert: Diferentes com cache clear
    assert settings1.APP_NAME == 'app1'
    assert settings2.APP_NAME == 'app2'
