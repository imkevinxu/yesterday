# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


def update_site_forward(apps, schema_editor):
    """Set site domain and name."""
    if settings.DEBUG:
        defaults={
            "domain": "localhost:8000",
            "name": "localhost"
        }
    else:
        defaults={
            "domain": settings.PROJECT_DOMAIN,
            "name": settings.PROJECT_NAME
        }

    Site = apps.get_model("sites", "Site")
    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults=defaults
    )


def update_site_backward(apps, schema_editor):
    """Revert site domain and name to default."""
    Site = apps.get_model("sites", "Site")
    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={
            "domain": "example.com",
            "name": "example"
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_site_forward, update_site_backward),
    ]
