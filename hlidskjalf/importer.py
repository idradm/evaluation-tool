import csv
from hlidskjalf.models import DataSet, DataItem, Item, Type

__author__ = 'adam'


class Importer():

    def __init__(self, name, filename):
        self.set = None
        self.name = name
        self.file = filename

    def run(self):
        self._create_set()
        if self.set is not None:
            with open(self.file, 'r') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    self._save(row)

    def _create_set(self):
        query = DataSet.objects.filter(name=self.name)
        if not query:
            self.set = DataSet(name=self.name)
            self.set.save()
        else:
            self.set = query[0]

    def _save(self, value):
        query = Item.objects.filter(name=value)
        if not query:
            item = Item(name=value)
            item.save()
        else:
            item = query[0]
        ditem = DataItem.objects.filter(item=item, set=self.set)
        if not ditem:
            DataItem(item=item, set=self.set).save()

    @staticmethod
    def add_type(name):
        query = Type.objects.filter(name=name)
        if not query:
            Type(name=name).save()