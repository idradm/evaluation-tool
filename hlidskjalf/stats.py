from hlidskjalf.models import DataItem, ResultItem


class Stats(object):

    @staticmethod
    def get_for_run(run):
        results = ResultItem.objects.filter(run=run)
        total = len(DataItem.objects.filter(set=run.set))
        found = len(results)
        coverage = round((float(found) / float(total)) * 100, 2)
        types = {}

        for result in results:
            if result.result is not None:
                if result.result.type is not None:
                    if result.result.type.name not in types:
                        types[result.result.type.name] = 0
                    types[result.result.type.name] += 1

        type_coverages = {}
        for type, value in types.items():
            type_coverages[type] = [
                value,
                round((float(value) / float(found)) * 100, 2)
            ]

        return {
            'total': total,
            'found': found,
            'coverage': coverage,
            'real_coverage': round(coverage * type_coverages['OK'] / 100, 2),
            'types': type_coverages
        }