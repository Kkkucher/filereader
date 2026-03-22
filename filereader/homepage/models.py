from django.db import models


class DataTable(models.Model):
    name = models.CharField(max_length=49)
    date = models.DateTimeField(null=True)
