from hlidskjalf.evals.eval import Eval
from hlidskjalf.models import DataItem, Result, ResultItem


class EpisodesEval(Eval):

    def _get_params(self, item, run):
        return {'seriesName': item.episodeitem.series, 'episodeName': item.episodeitem.name, 'cb': run.id}

    @staticmethod
    def _save_result(item, out, run):
        val = Eval._parse_url(out['url'])
        query = Result.objects.filter(item=item, value=val)
        if not query:
            result = Result(item=item, value=val)
            result.save()
        else:
            result = query[0]
        data_item = DataItem.objects.filter(item=item, set=run.set)[0]
        ResultItem(item=data_item, result=result, run=run).save()