from django.contrib import admin

from .models import SecTest, SecTestSuite

# Register your models here.
admin.site.register([SecTest, SecTestSuite])
