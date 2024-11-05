from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=100)
    max_biowaste = models.PositiveIntegerField(default=0)
    max_glass = models.PositiveIntegerField(default=0)
    max_plastic = models.PositiveIntegerField(default=0)
    total_biowaste = models.PositiveIntegerField(default=0)
    total_glass = models.PositiveIntegerField(default=0)
    total_plastic = models.PositiveIntegerField(default=0)

class Storage(models.Model):
    name = models.CharField(max_length=100)
    max_biowaste = models.PositiveIntegerField(default=0)
    max_glass = models.PositiveIntegerField(default=0)
    max_plastic = models.PositiveIntegerField(default=0)
    current_biowaste = models.PositiveIntegerField(default=0)
    current_glass = models.PositiveIntegerField(default=0)
    current_plastic = models.PositiveIntegerField(default=0)

class Distance(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    distance = models.PositiveIntegerField()

