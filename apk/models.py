from django.db import models

# Create your models here.


class Campaign_id(models.Model):
    campaign_id = models.CharField(max_length=100, null=True, blank=True)
