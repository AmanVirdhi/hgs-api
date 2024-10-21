from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.

class Signup(models.Model):
    username = models.CharField(max_length=255, unique=True)  # Unique username
    email = models.EmailField(unique=True)                    # Unique email address
    password = models.CharField(max_length=128)               # Hashed password

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Hash the password before saving to the database
        if self.password:
            self.password = make_password(self.password)
        super(Signup, self).save(*args, **kwargs)

class Grievance(models.Model):
    name = models.CharField(max_length=255)  # Name of the person filing the grievance
    hgstypes = models.CharField(max_length=50)  # Type of grievance (e.g., "messes")
    room = models.IntegerField()  # Room number (max length = 4)
    course = models.CharField(max_length=50)  # Course name (e.g., "mca")
    mobile = models.CharField(max_length=10)  # Mobile number (max length)
    description = models.TextField()  # Description of the grievance

    def __str__(self):
        return f"{self.name} - {self.hgstypes} - {self.room}"
