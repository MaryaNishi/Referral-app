from django.db import models

# Create your models here.
class User(models.Model):
    phone_number = models.CharField(max_length=16, unique=True)
    invite_code = models.CharField(max_length=6, unique=True)
    activated_invite_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f"{self.phone_number} with invide code: {self.invite_code}"
    
