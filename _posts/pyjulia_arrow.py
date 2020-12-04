from julia import Arrow
import pandas as pd
import tracemalloc
from timeit import repeat

def pyjulia_alloc(fpath):
    data = Arrow.Table(fpath)
    tracemalloc.start()
    pd.DataFrame(data)
    snap = tracemalloc.take_snapshot()
    snapshot = snap.filter_traces(
        (
            tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
            tracemalloc.Filter(False, "<unknown>"),
        )
    )
    stats = snapshot.statistics("lineno")
    total = sum(stat.size for stat in stats)
    tracemalloc.stop()
    print("Total allocations: %.1f KiB" % (total / 1024))


eeg_arrow_data = "/home/src/Projects/neuriviz/data/exp_pro/sub-002/ses-01/eeg/sub-002_ses-01_task-gonogo_run-01_eeg.arrow"

runs = 10
evals = 1
pyjulia_alloc(eeg_arrow_data)
data = Arrow.Table(eeg_arrow_data)

stats = repeat(stmt="pd.DataFrame(data)", repeat=runs, number = evals, globals=globals())
print("--------------")
print("Mean time: %.5f s" % (sum(stats) / runs))
print("Max time: %.5f s" % max(stats))
print("Min time: %.5f s" % min(stats))
print("--------------")
print("Samples: {}".format(runs))
print("Evals/Sample: {}".format(evals))
