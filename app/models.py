import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, User


class Administrator(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_picture = models.ImageField(default="default_profile_picture.png")
    pass

    @property
    def image_url(self) -> str:
        if self.profile_picture and hasattr(self.profile_picture, "url"):
            return self.profile_picture.url
        else:
            return ""


class Tech(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    username = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self) -> str:
        return self.username


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    username = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self) -> str:
        return self.username


class Application(models.Model):
    STATUS = (
        ("Waiting ...", "Waiting ..."),
        ("Expecting a visit!", "Expecting a visit!"),
        ("In progress ...", "In progress ..."),
        ("Completed", "Completed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, related_name='user_likes', on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    address = models.CharField(max_length=30, null=False, blank=False)
    image = models.ImageField(default="application.jpg", null=False, blank=False)
    status = models.CharField(max_length=18, choices=STATUS, default="Waiting ...")
    date_of_visit_by_technician = models.DateField(null=False, blank=False)
    technician = models.ForeignKey(Tech, on_delete=models.CASCADE, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    @property
    def image_url(self) -> str:
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        else:
            return ""
