from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class Feedback(TimeStampedModel):
    ease_of_use = models.PositiveSmallIntegerField()
    likeliness_of_recommend = models.PositiveSmallIntegerField()
    overall_score = models.PositiveSmallIntegerField()
    proposed_price = models.FloatField()
    open_feedback = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)

    def __str__(self):
        return f"[{self.pk}]{self.user.username}"
