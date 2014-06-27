from django.db import models


# Create your models here.
class DataSet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=5)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.lang.upper())


class Item(models.Model):
    real_type = models.CharField(max_length=100)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.real_type = self.__class__.__name__.lower()
        super(Item, self).save()


class MovieItem(Item):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class EpisodeItem(Item):
    name = models.CharField(max_length=255)
    series = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s/%s" % (self.series, self.name)


class Type(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
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

    def __unicode__(self):
        return self.value


class Run(models.Model):
    url = models.CharField(max_length=255)
    set = models.ForeignKey(DataSet)


class DataItem(models.Model):
    item = models.ForeignKey(Item)
    set = models.ForeignKey(DataSet)

    def __unicode__(self):
        return "%s:%s" % (self.set.name, self.item)


class ResultItem(models.Model):
    item = models.ForeignKey(DataItem)
    result = models.ForeignKey(Result, blank=True, null=True)
    run = models.ForeignKey(Run, blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.item, self.run.url)


class Stat(models.Model):
    run = models.ForeignKey(Run)
    total = models.IntegerField()
    found = models.IntegerField()
    type = models.ForeignKey(Type, blank=True, null=True)
