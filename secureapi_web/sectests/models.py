from django.conf import settings
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel


class SecError(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    description = models.TextField()
    title = models.CharField(max_length=128)

    def __str__(self):
        return "({}){}".format(self.code, self.title)


class SecTest(models.Model):
    RESULTS = Choices('passed', 'failed', 'error')
    result = StatusField(choices_name='RESULTS')
    error_code = models.ForeignKey('sectests.SecError', on_delete=models.DO_NOTHING)


class SecTestSuite(TimeStampedModel):
    tests = models.ManyToManyField('sectests.SecTest')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    security_index = models.FloatField(null=True)

    def calculate_security_index(self):
        failed_test = self.tests.filter(result="failed").count()
        all_tests = self.tests.objects.count()
        return (all_tests - failed_test) / failed_test

    class Meta:
        ordering = ('-modified', )


@receiver(m2m_changed, sender=SecTestSuite.tests.through)
def video_category_changed(sender, instance, action, **kwargs):
    if action in ['post_remove', 'post_add']:
        instance.security_index = instance.calculate_security_index()
        instance.save()
