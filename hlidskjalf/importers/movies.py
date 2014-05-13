from hlidskjalf.importers.importer import Importer
from hlidskjalf.models import DataItem, Item


class MoviesImporter(Importer):

    def __init__(self, name, filename):
        super(MoviesImporter, self).__init__(name, filename)

    def _save(self, row):
        value = row[0]
        query = Item.objects.filter(name=value)
        if not query:
            item = Item(name=value)
            item.save()
        else:
            item = query[0]
        ditem = DataItem.objects.filter(item=item, set=self.set)
        if not ditem:
            DataItem(item=item, set=self.set).save()
            return item.name