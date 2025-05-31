from django.db import models
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.role})"