from mock import patch
from django.test import TestCase
from hlidskjalf.importer import Importer
from hlidskjalf.models import DataSet, DataItem, Item, Result
from hlidskjalf.lidskjalf import Lidskjalf


# Create your tests here.
class ImporterTestCase(TestCase):

    def test_correct_set_created(self):
        set_name = 'test'
        importer = Importer(set_name, "hlidskjalf/test/test_import.csv")
        importer.run()
        query = DataSet.objects.filter(name=set_name)
        self.assertEqual(set_name, query[0].name)
        data_items = DataItem.objects.filter(set=query[0])
        self.assertEqual(6, len(data_items))

        importer.run()
        query = DataSet.objects.filter(name=set_name)
        self.assertEqual(1, len(query))
        data_items = DataItem.objects.filter(set=query[0])
        self.assertEqual(6, len(data_items))

        items = Item.objects.all()
        self.assertEqual(6, len(items))


class EvaluationTestCase(TestCase):

    def test_url_builder(self):
        set_name = 'test'
        importer = Importer(set_name, "hlidskjalf/test/test_import.csv")
        importer.run()
        tool = Lidskjalf()

        tool.set_entry_point('http://wikiaglobal.adam.wikia-dev.com/api/v1/Tv/Movie')
        with patch.object(tool, '_get', return_value={'url': 'http://testoutput'}):
            tool.run(set_name)

        query = Result.objects.all()
        self.assertEqual(6, len(query))