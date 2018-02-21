from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list


class MeditorModel(models.Model):
    """ Basic metadata for Meditor objects """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=1024, default='', null=True, blank=True)

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class DataSourceType(MeditorModel):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class MetricData(MeditorModel):
    # Name of the metric in Elasticsearch with the data for the metric
    implementation = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return  self.implementation


class Metric(MeditorModel):
    name = models.CharField(max_length=200, unique=True)
    data = models.ForeignKey(MetricData, on_delete=models.CASCADE, null=True, blank=True)

    data_source_type = models.ForeignKey(DataSourceType,
                                         on_delete=models.CASCADE, null=True, blank=True)

    thresholds = models.CharField(max_length=200, default=None, null=True, blank=True,
                                  validators=[validate_comma_separated_integer_list])

    def __str__(self):
        return  self.name


class Factoid(MeditorModel):
    name = models.CharField(max_length=200, unique=True)

    data_source_type = models.ForeignKey(DataSourceType,
                                         on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Attribute(MeditorModel):
    name = models.CharField(max_length=200, unique=True)
    # Relations
    metrics = models.ManyToManyField(Metric, blank=True)
    factoids = models.ManyToManyField(Factoid, blank=True)
    subattributes = models.ManyToManyField("Attribute", blank=True)

    def __str__(self):
        return self.name


class Goal(MeditorModel):
    name = models.CharField(max_length=200, unique=True)
    # Relations
    attributes = models.ManyToManyField(Attribute)
    subgoals = models.ManyToManyField("Goal", blank=True)

    def __str__(self):
        return self.name


class QualityModel(MeditorModel):
    """ Quality Model (maturity, Health ...)"""
    name = models.CharField(max_length=200, unique=True)
    # Relations
    goals = models.ManyToManyField("Goal")

    def __str__(self):
        return self.name
