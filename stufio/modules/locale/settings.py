# Example module settings_metadata.py for a locale module

from stufio.core.setting_registry import (
    GroupMetadata, SubgroupMetadata, SettingMetadata, 
    SettingType, settings_registry
)


"""Register settings for this module"""
# Register a new group tab for this module
settings_registry.register_group(
    GroupMetadata(
        id="localization", 
        label="Localization", 
        icon="globe", 
        order=45,  # Between API and Database
    )
)
    
# Register subgroups
settings_registry.register_subgroup(
    SubgroupMetadata(
        id="general",
        group_id="localization",
        label="General Localization",
        order=10
    ),
)

settings_registry.register_subgroup(
    SubgroupMetadata(
        id="advanced",
        group_id="localization",
        label="Advanced Localization",
        order=20
    ),
)
    
# Register settings
settings_registry.register_setting(
    SettingMetadata(
        key="locale_DEFAULT_LOCALE",
        label="Default Locale",
        description="The default locale for new users",
        group="localization",
        subgroup="general",
        type=SettingType.SELECT,
        options=[
            {"label": "English", "value": "en"},
            {"label": "Français", "value": "fr"},
            {"label": "Español", "value": "es"},
            {"label": "Deutsch", "value": "de"},
            {"label": "Polski", "value": "pl"},
        ],
        order=10,
        module="locale"
    )
)