from django.apps import AppConfig


class CommoditiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'commodities'
    
class MediasCommoditiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medias_commodities'
