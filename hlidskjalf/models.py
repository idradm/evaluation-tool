from django.db import models


# Create your models here.
class DataSet(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Result(models.Model):
    value = models.CharField(max_length=255)
    item = models.ForeignKey(Item)
    type = models.ForeignKey(Type, blank=True, null=True)

    def set_type(self, type_name):
        type = Type.objects.filter(name=type_name)
        if type:
            self.type = type[0]
            self.save()

    def __str__(self):
        return self.value


class Run(models.Model):
    url = models.CharField(max_length=255)
    set = models.ForeignKey(DataSet)


class DataItem(models.Model):
    item = models.ForeignKey(Item)
    set = models.ForeignKey(DataSet)

    def __str__(self):
        return "%s:%s" % (self.set.name, self.item.name)


class ResultItem(models.Model):
    item = models.ForeignKey(DataItem)
    result = models.ForeignKey(Result, blank=True, null=True)
    run = models.ForeignKey(Run, blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.item, self.run.url)