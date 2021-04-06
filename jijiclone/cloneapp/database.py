from decouple import config


def generate_database(debug):
    if debug:
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config('DB_NAME'),
                'USER': config('DB_USER'),
                'PASSWORD': config('DB_PASSWORD'),
                'HOST': config('DB_HOST'),
                'PORT': config('DB_PORT', cast=int),
            }
        }
    else:
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'DATABASE_URL': config('DATABASE_URL')
            }
        }
