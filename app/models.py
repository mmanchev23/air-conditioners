import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ("Administrator", "Administrator"),
        ("Tech", "Tech"),
        ("Customer", "Customer"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_picture = models.ImageField(default="default_profile_picture.png")
    role = models.CharField(max_length=13, choices=ROLES, default="Customer")
    pass

    def __str__(self) -> str:
        return self.username

    @property
    def image_url(self) -> str:
        if self.profile_picture and hasattr(self.profile_picture, "url"):
            return self.profile_picture.url
        else:
            return ""


class Application(models.Model):
    STATUS = (
        ("Waiting ...", "Waiting ..."),
        ("Expecting a visit!", "Expecting a visit!"),
        ("In progress ...", "In progress ..."),
        ("Completed", "Completed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    address = models.CharField(max_length=30, null=False, blank=False)
    image = models.ImageField(default="application.jpg")
    status = models.CharField(max_length=18, choices=STATUS, default="Waiting ...")
    date_of_visit_by_technician = models.DateField(null=True, blank=True)
    technician = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return self.title

    @property
    def image_url(self) -> str:
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        else:
            return ""
