from __future__ import absolute_import

from factory import LazyAttributeSequence, Sequence
from factory.django import DjangoModelFactory

from .models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = LazyAttributeSequence(lambda o, n: '%s-user-%s@django.com' % (o.name.split()[0].lower(), n))
    name = Sequence(lambda n: 'User #%s' % n)
    password = 'password'

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        manager = cls._get_manager(target_class)
        return manager.create_user(*args, **kwargs)


class AdminUserFactory(UserFactory):
    email = LazyAttributeSequence(lambda o, n: '%s-admin-%s@django.com' % (o.name.split()[0].lower(), n))

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        manager = cls._get_manager(target_class)
        return manager.create_superuser(*args, **kwargs)
