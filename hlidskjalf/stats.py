from hlidskjalf.models import DataItem, ResultItem, Stat, Type


class Stats(object):

    @staticmethod
    def get(run):
        stats = Stat.objects.filter(run=run)

        total, found, coverage = (0, 0, 0)
        type_coverages = {}
        for stat in stats:
            if stat.type:
                type_coverages[stat.type.name] = [
                    stat.found,
                    round((float(stat.found) / float(stat.total)) * 100, 2)
                ]
            else:
                total = stat.total
                found = stat.found
                coverage = round((float(found) / float(total)) * 100, 2)

        return {
            'total': total,
            'found': found,
            'coverage': coverage,
            'real_coverage': round(coverage * type_coverages['OK'][1] / 100, 2),
            'types': type_coverages
        }

    @staticmethod
    def calculate(run):
        results = ResultItem.objects.filter(run=run)
        total = len(DataItem.objects.filter(set=run.set))
        found = len(results)
        Stats.save(run, None, (total, found))
        types = {}

        for result in results:
            if result.result is not None:
                if result.result.type is not None:
                    if result.result.type.name not in types:
                        types[result.result.type.name] = 0
                    types[result.result.type.name] += 1

        for type, value in types.items():
            Stats.save(run, Type.objects.get(name=type), (found, value))

    @staticmethod
    def save(run, type, values):
        (total, found) = values
        stat = Stat.objects.filter(run=run, type=type)
        if not stat:
            stat = Stat(run=run, type=type)
        else:
            stat = stat[0]
        stat.total = total
        stat.found = found
        stat.save()
