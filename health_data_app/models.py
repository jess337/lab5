from django.db import models

class MedicalData(models.Model):
    patient_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    diagnosis = models.TextField()
    date = models.CharField()

    def __str__(self):
        return self.name
# Create your models here.
