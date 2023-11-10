from .settings import *

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv("AZURE_SQL_DATABASE"),
        'HOST': os.getenv("AZURE_SQL_SERVER"),
        'PORT': '1433',
        'USER': os.getenv("AZURE_SQL_USER"),
        'PASSWORD': os.getenv("AZURE_SQL_PASSWORD"),
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
        },
    }
}

DEBUG = True
