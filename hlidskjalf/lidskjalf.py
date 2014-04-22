import requests
from hlidskjalf.models import DataSet, DataItem, Result


class Lidskjalf():

    def set_entry_point(self, url):
        self.url = url

    def run(self, set_name):
        set = self._get_set(set_name)
        if set:
            for data_item in self._get_items(set):
                out = self._get({'movieName': data_item.item.name})
                if out:
                    self._save_result(data_item.item, out)

    def _get(self, params):
        r = requests.get(self.url, params=params)
        if r.status_code == 200:
            return r.json()
        return False

    @staticmethod
    def _get_set(set_name):
        return DataSet.objects.filter(name=set_name)

    @staticmethod
    def _get_items(set):
        return DataItem.objects.filter(set=set)

    @staticmethod
    def _save_result(item, out):
        query = Result.objects.filter(item=item)
        if not query:
            Result(item=item, value=out['url']).save()