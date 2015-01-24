from django.db.models import TextField

from model_utils.models import TimeStampedModel

from django_extensions.db.fields import UUIDField


class Story(TimeStampedModel):
    uuid = UUIDField(unique=True, null=False)
    story = TextField()

    def __unicode__(self):
        return self.uuid
