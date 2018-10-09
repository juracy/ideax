from django.core.management import call_command
from django.utils import translation
from pytest import fixture

pytest_plugins = [
    'ideax.tests.fixtures',
    'ideax.ideax.tests.fixtures',
]


@fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'docker/initialdata.json')


@fixture(autouse=True)
def set_default_language():
    translation.activate('pt-br')
