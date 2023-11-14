from .settings import *

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("AZURE_MYSQL_NAME"),
        'HOST': os.getenv("AZURE_MYSQL_HOST"),
        'PORT': '3306',
        'USER': os.getenv("AZURE_MYSQL_USER"),
        'PASSWORD': os.getenv("AZURE_MYSQL_PASSWORD"),
    }
}

DEBUG = True
