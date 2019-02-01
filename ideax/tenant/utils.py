from django.core.management import call_command
from django.db import connection
from tenant_schemas.utils import get_tenant_model
from ideax.settings.django._core import PATH_FILE_INIT_DATA


def get_tenant(model, hostname):
    return model.objects.get(domain_url=hostname)


def set_connection(request, hostname):
    set_connection_public_schema()

    TenantModel = get_tenant_model()

    tenant = get_tenant(TenantModel, hostname)
    assert isinstance(tenant, TenantModel)

    request.tenant = tenant
    set_connection_by_tenant(request.tenant)


def set_connection_by_tenant(tenant):
    connection.set_tenant(tenant)


def set_connection_public_schema():
    connection.set_schema_to_public()


def load_init_data():
    if PATH_FILE_INIT_DATA:
        call_command('loaddata', PATH_FILE_INIT_DATA)
