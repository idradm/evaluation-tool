from django.db import models


# Create your models here.
class DataSet(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)


class DataItem(models.Model):
    item = models.ForeignKey(Item)
    set = models.ForeignKey(DataSet)


class Result(models.Model):
    value = models.CharField(max_length=255)
    item = models.ForeignKey(Item)

