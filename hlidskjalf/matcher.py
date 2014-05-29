import urllib
from hlidskjalf.models import Type


class EpisodesMatcher():
    def __init__(self):
        self.ok = Type.objects.get(name='OK')

    def match(self, result_item):
        parsed_url = str(urllib.unquote(result_item.result.value).decode('utf8')).lower()
        if (parsed_url.find(str(result_item.result.item.episodeitem.series).lower().replace(' ', '')) >= 0 and
                parsed_url.find(str(result_item.result.item.episodeitem.name).lower().replace(' ', '_')) >= 0):
            result_item.result.type = self.ok
            result_item.result.save()
            return True
        return False