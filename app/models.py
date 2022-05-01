import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, User


class User(AbstractUser):
    ROLES = (
        ("Administrator", "Administrator"),
        ("Tech", "Tech"),
        ("Customer", "Customer"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=13, choices=ROLES, default="Customer")
    pass
