# Modules
import uuid



# Models
from django.db import models



class BaseModel(models.Model):
    unique_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    
    
    class Meta:
        abstract = True