from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # Champs personnalisés à ajouter plus tard
    date_naissance = models.DateField(null=True, blank=True)
    score_total = models.IntegerField(default=0)  # exemple futur

    def __str__(self):
        return self.username