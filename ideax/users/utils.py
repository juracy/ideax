from django.http.response import Http404
from django.db import connection

from tenant_schemas.utils import get_tenant_model


def get_tenant(model, hostname):
    return model.objects.get(domain_url=hostname)


def set_connection(request, hostname):
    connection.set_schema_to_public()

    TenantModel = get_tenant_model()
    try:
        tenant = get_tenant(TenantModel, hostname)
        assert isinstance(tenant, TenantModel)
    except TenantModel.DoesNotExist:
        raise Http404('No tenant for {!r}'.format(request.get_host()))
    except AssertionError:
        raise Http404('Invalid tenant {!r}'.format(request.tenant))

    request.tenant = tenant
    connection.set_tenant(request.tenant)
