import os
import sys
from coranno.settings import DATABASES
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coranno.settings")
application = get_wsgi_application()

def create_super_user_if_not_exists(user, password):
    import django
    django.setup()

    try:
        from django.contrib.auth.models import User
        u = User(username=user)
        u.set_password(password)
        u.is_superuser = True
        u.is_staff = True
        u.save()
        print('created super user {}'.format(user))
    except django.db.utils.IntegrityError:
        print('super user exists {}'.format(user))


if __name__ == "__main__":

    call_command('makemigrations')
    call_command('migrate', '--noinput')

    create_super_user_if_not_exists(os.getenv('DJANGO_SU_NAME', 'admin'),
        os.getenv('DJANGO_SU_PASSWORD', 'admin'))
    
    call_command('runserver', sys.argv[1])

