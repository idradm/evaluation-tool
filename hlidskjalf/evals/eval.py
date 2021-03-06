import re
from __builtin__ import xrange
import requests
from django import db
from multiprocessing.pool import ThreadPool
from hlidskjalf.models import DataSet, DataItem, Run


class Eval(object):

    batch_size = 10000

    def set_entry_point(self, url):
        self.url = url

    def run(self, set_name, processes=5):
        run = self._get_run(set_name)
        if run:
            items = self._get_items(run)
            for i in xrange(0, len(items), self.batch_size):
                threads = ThreadPool(processes=processes)
                threads.map(self._run_batch, items[i:i+self.batch_size], processes)
                db.reset_queries()
        return True

    def _run_batch(self, params):
        (data_item, run) = params
        out = self._get(self._get_params(data_item.item, run))
        if out:
            self._save_result(data_item.item, out, run)

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

    def _get_params(self, item, run):
        pass

    @staticmethod
    def _get_set(set_name):
        return DataSet.objects.filter(name=set_name)

    @staticmethod
    def _get_items(run):
        items = DataItem.objects.filter(set=run.set)
        result = []
        for item in items:
            result.append((item, run))
        return result

    @staticmethod
    def _save_result(item, out, run):
        pass

    @staticmethod
    def _parse_url(url):
        return re.sub(r'sandbox-s\d\.', '', url)