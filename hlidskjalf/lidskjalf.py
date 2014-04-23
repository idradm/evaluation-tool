import requests
from hlidskjalf.models import DataSet, DataItem, Result, Run, ResultItem


class Lidskjalf():

    def set_entry_point(self, url):
        self.url = url

    def run(self, set_name):
        result = []
        run = self._get_run(set_name)
        if run:
            for data_item in self._get_items(run.set):
                out = self._get({'movieName': data_item.item.name})
                if out:
                    result.append("%s with url %s added" % (data_item.item.name, out['url']))
                    self._save_result(data_item.item, out, run)
        return result

    def _get(self, params):
        r = requests.get(self.url, params=params)
        if r.status_code == 200:
            return r.json()
        return False

    def _get_run(self, set_name):
        set = self._get_set(set_name)
        if set:
            run = Run(set=set[0], url=self.url)
            run.save()
            return run
        return False

    @staticmethod
    def _get_set(set_name):
        return DataSet.objects.filter(name=set_name)

    @staticmethod
    def _get_items(set):
        return DataItem.objects.filter(set=set)

    @staticmethod
    def _save_result(item, out, run):
        val = out['url']
        query = Result.objects.filter(item=item, value=val)
        if not query:
            result = Result(item=item, value=val)
            result.save()
        else:
            result = query[0]
        item = DataItem.objects.filter(item=item, set=run.set)[0]
        ResultItem(item=item, result=result, run=run).save()