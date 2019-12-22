# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class SecTest(TimeStampedModel):
    id = models.AutoField(primary_key=True)  # AutoField?
    result = models.IntegerField()
    code = models.TextField()
    suite = models.ForeignKey("SecTestSuite", models.DO_NOTHING, db_column="suite")

    class Meta:
        db_table = "sectest"


class SecTestSuite(TimeStampedModel):
    id = models.CharField(primary_key=True, max_length=128)  # AutoField?
    url = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)

    class Meta:
        db_table = "sectestsuite"
