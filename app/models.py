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


class Application(models.Model):
    STATUS = (
        ("Waiting ...", "Waiting ..."),
        ("Expecting a visit!", "Expecting a visit!"),
        ("In progress ...", "In progress ..."),
        ("Completed", "Completed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    address = models.CharField(max_length=30, null=False, blank=False)
    image = models.ImageField(default="application.jpg", null=False, blank=False)
    status = models.CharField(max_length=18, choices=STATUS, default="Waiting ...")
    date_of_visit_by_technician = models.DateField(null=False, blank=False)
    technician = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
