from django.db import models
from django.conf import settings


class Site(models.Model):
    # Assuming you have already defined fields like `user` and `name`
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField()

    class Meta:
        unique_together = ('user', 'name',)
        # This ensures that each user can only have one unique name for a site