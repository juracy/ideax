from django.db import models
from django.db import models
from tenant_schemas.models import TenantMixin

# Create your models here.
class Client(TenantMixin):
    name = models.CharField(max_length=100)        
    created_on = models.DateField(auto_now_add=True)
    on_trial = models.BooleanField()
    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True