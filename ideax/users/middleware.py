import django

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import DisallowedHost
from django.db import connection
from django.http import Http404

from ideax.tenant.utils import set_connection

from tenant_schemas.utils import (get_tenant_model, remove_www,
                                  get_public_schema_name)
from tenant_schemas.middleware import TenantMiddleware, MIDDLEWARE_MIXIN


class EmailTenantMiddleware(TenantMiddleware):
    def process_request(self, request):
        # Connection needs first to be at the public schema, as this is where
        # the tenant metadata is stored.

        if 'client' in request.COOKIES:
            hostname = request.COOKIES['client']
        else:
            hostname = self.hostname_from_request(request)

        set_connection(request, hostname)
        # Do we have a public-specific urlconf?
        if hasattr(settings, 'PUBLIC_SCHEMA_URLCONF') and request.tenant.schema_name == get_public_schema_name():
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF

class TenantCookieMiddleware(MIDDLEWARE_MIXIN):
    def process_response(self, request, response):
        if hasattr(request, 'session') and request.session.get('client'):
            response.set_cookie('client', request.session.get('client'))
        return response
