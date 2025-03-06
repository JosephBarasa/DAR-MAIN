from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Users'
    
    # connecting signals
    
    def ready(self):
         #imports signals when the app is ready
        import Users.signals  
