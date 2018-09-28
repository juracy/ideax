from .settings import *


# Usamos o backend em memória para facilitar os testes
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
