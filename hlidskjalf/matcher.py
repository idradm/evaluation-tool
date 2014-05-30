import re
import string
import urllib
from hlidskjalf.models import Type


class EpisodesMatcher():
    def __init__(self):
        self.ok = Type.objects.get(name='OK')

    def match(self, result_item):
        parsed_url = EpisodesMatcher.normalize(urllib.unquote(result_item.result.value))
        episodes = result_item.result.item.episodeitem.name.split(';')
        for episode in episodes:
            if (parsed_url.find(EpisodesMatcher.normalize(result_item.result.item.episodeitem.series)) >= 0 and
                    parsed_url.find(EpisodesMatcher.normalize(episode)) >= 0):
                result_item.result.type = self.ok
                result_item.result.save()
                return True
        return False

    @staticmethod
    def normalize(text):
        return re.sub("[%s]" % string.punctuation, '', re.sub('\s+', '', text.lower()))