import uuid
from django.db import models

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # REQUIRED fields per checklist:
    name = models.CharField(max_length=100)          # CharField
    price = models.IntegerField()                    # IntegerField
    description = models.TextField()                 # TextField
    thumbnail = models.URLField()                    # URLField
    category = models.CharField(max_length=50)       # CharField
    is_featured = models.BooleanField(default=False) # BooleanField

    def __str__(self):
        return f"{self.name} (Rp{self.price})"
