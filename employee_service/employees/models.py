from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.role}"
