from authtools.models import AbstractNamedUser


class User(AbstractNamedUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
