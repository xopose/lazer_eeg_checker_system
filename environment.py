from decouple import config


if config("ENVIRONMENT") == "dev":
    SETTINGS_MODULE = "lazer-mne.settings.development"
if config("ENVIRONMENT") == "prod":
    SETTINGS_MODULE = "lazer-mne.settings.production"
