from django.db import models


class SecSolution(models.Model):
    code = models.CharField(max_length=25, primary_key=True)
    solution = models.TextField()
    owasp_link = models.URLField()

    def __str__(self):
        return self.code
