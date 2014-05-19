import csv
import sys
from hlidskjalf.models import DataSet, Type


class Importer(object):

    def __init__(self, name, filename):
        self.set = None
        self.name = name
        self.file = filename

    def run(self):
        result = []
        self._create_set()
        if self.set is not None:
            csv.field_size_limit(sys.maxsize)
            with open(self.file, 'r') as csv_file:
                reader = csv.reader(csv_file, delimiter="\t")
                for row in reader:
                    response = self._save(row)
                    if response:
                        result.append(response)
        return result

    def _create_set(self):
        query = DataSet.objects.filter(name=self.name)
        if not query:
            self.set = DataSet(name=self.name)
            self.set.save()
        else:
            self.set = query[0]

    def _save(self, row):
        raise Exception("Not implemented")

    @staticmethod
    def add_type(name):
        query = Type.objects.filter(name=name)
        if not query:
            Type(name=name).save()