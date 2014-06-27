from hlidskjalf.importers.importer import Importer
from hlidskjalf.models import DataItem, EpisodeItem


class EpisodeImporter(Importer):

    def _save(self, row):
        if len(row[0]) < 255 and len(row[1]) < 255:
            query = EpisodeItem.objects.filter(series=row[0], name=row[1])
            if not query:
                item = EpisodeItem(series=row[0], name=row[1])
                item.save()
            else:
                item = query[0]
            ditem = DataItem.objects.filter(item=item, set=self.set)
            if not ditem:
                DataItem(item=item, set=self.set).save()
                return item.name