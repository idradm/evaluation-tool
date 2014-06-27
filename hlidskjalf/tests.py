from mock import patch
from django.test import TestCase, TransactionTestCase
from hlidskjalf.importers.movies import MoviesImporter
from hlidskjalf.importers.episodes import EpisodeImporter
from hlidskjalf.models import DataSet, DataItem, Item, Result
from hlidskjalf.evals.movies import MoviesEval
from hlidskjalf.evals.episodes import EpisodesEval


# Create your tests here.
class ImporterTestCase(TestCase):

    def test_correct_movies_set_created(self):
        set_name = 'test'
        importer = MoviesImporter(set_name, "hlidskjalf/test/test_import.csv")
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

    def test_correct_episode_set_created(self):
        set_name = 'episode_test'
        importer = EpisodeImporter(set_name, "hlidskjalf/test/test_tv_import.csv")
        importer.run()

        query = DataSet.objects.filter(name=set_name)
        self.assertEqual(set_name, query[0].name)
        data_items = DataItem.objects.filter(set=query[0])
        self.assertEqual(40, len(data_items))

        importer.run()
        query = DataSet.objects.filter(name=set_name)
        self.assertEqual(1, len(query))
        data_items = DataItem.objects.filter(set=query[0])
        self.assertEqual(40, len(data_items))

        items = Item.objects.all()
        self.assertEqual(40, len(items))


class EvaluationTestCase(TransactionTestCase):

    def test_url_builder(self):
        set_name = 'test'
        importer = MoviesImporter(set_name, "hlidskjalf/test/test_import.csv")
        importer.run()
        tool = MoviesEval()

        tool.set_entry_point('http://wikiaglobal.adam.wikia-dev.com/api/v1/Tv/Movie')
        with patch.object(tool, '_get', return_value={'url': 'http://testoutput'}):
            tool.run(set_name)

        query = Result.objects.all()
        self.assertEqual(6, len(query))

    def test_episode_eval(self):
        set_name = 'test'
        lang = 'en'
        importer = EpisodeImporter(set_name, "hlidskjalf/test/test_tv_import.csv", lang)
        importer.run()

        tool = EpisodesEval()
        tool.set_entry_point('http://sandbox-s3.www.wikia.com/api/v1/Tv/Movie')
        with patch.object(tool, '_get', return_value={'url': 'http://sandbox-s3.www.wikia.com'}):
            tool.run(set_name)

        set = DataSet.objects.get(name=set_name)
        self.assertEqual(set.lang, lang)

        query = Result.objects.all()
        self.assertEqual(40, len(query))