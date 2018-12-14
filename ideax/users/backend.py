from django_auth_ldap.backend import *
from .models import AuthConfiguration


class LDAPBackendByTenant(LDAPBackend):

    def authenticate(self, request=None, username=None, password=None, **kwargs):
        configuration = AuthConfiguration.objects.get(active=True)

        ldap = LDAPBackend()
        ldap_se = LDAPSearch(base_dn=configuration.user_search_base,
                             scope=2,
                             filterstr=configuration.user_filter)

        di = dict()
        di['USER_SEARCH']=ldap_se
        di['BIND_DN']=configuration.bind_dn
        di['BIND_PASSWORD']=configuration.bind_password
        di['SERVER_URI']=configuration.host        

        settings = LDAPSettings(defaults=di)
        ldap.settings = settings

        return ldap.authenticate(request,
                                 request.POST.get('username',''),
                                 request.POST.get('password',''))
