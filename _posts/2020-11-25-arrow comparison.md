---
title: "Introduction to Apache Arrow in Julia and Python"
image:
  path: /assets/brain_tiles.png
comments: true
share: true
tags:
    - julia
    - python
    - arrow
---

I greatly enjoy programming in Julia and Python.
The language I most often reach for nowadays is Julia for data exploration and analysis.
However, I also work in Python on other projects and endeavors - as does most of the world!
Thankfully, these two programming ecosystems don't have to be mutually exclusive of one another thanks to

The Arrow format was created in 2016 by Wes McKinney, the creator of the extremely popular [`pandas`](https://pandas.pydata.org/) Python package, to produce language-independent open standards and libraries to accelerate and simplify in-memory computing. [6]
Of note, it is ideal for columnar data, cache-efficiency on CPUs and GPUs, leverages parallel processing, and optimized for scan and random access.
`Arrow.jl` brilliantly used memory mapping to implement the standard in an immensely efficient way.
To address the issue of the file format, I turned to [`Arrow.jl`](https://github.com/JuliaData/Arrow.jl), which is maintained by the [JuliaData organization](https://github.com/JuliaData), to use the Apache Arrow format.

[6] Wes McKinney, Apache Arrow and the Future of Data Frames. 2020.


6399640

# Benchmarking Reading of an Arrow File

```jl
using Arrow
using BenchmarkTools
using DataFrames

eeg_arrow_data = "/path/to/data.arrow"

@benchmark Arrow.Table($eeg_arrow_data) |> DataFrame;
```

If the expression you want to benchmark depends on external variables, you should use $ to "interpolate" them into the benchmark expression to avoid the problems of benchmarking with globals. Essentially, any interpolated variable $x or expression $(...) is "pre-computed" before benchmarking begins:
https://github.com/JuliaCI/BenchmarkTools.jl

```
  memory estimate:  109.30 KiB
  allocs estimate:  1860
  --------------
  minimum time:     114.013 μs (0.00% GC)
  median time:      117.280 μs (0.00% GC)
  mean time:        133.582 μs (7.45% GC)
  maximum time:     6.412 ms (76.09% GC)
  --------------
  samples:          10000
  evals/sample:     1
```


```python
from pyarrow import feather
import tracemalloc
from timeit import repeat

def pyarrow_alloc(fpath):
    tracemalloc.start()
    feather.read_feather(fpath)
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

eeg_arrow_data = "/path/to/data.arrow"
runs = 10000
evals = 1

pyarrow_alloc(eeg_arrow_data)

stats = repeat(
    stmt="feather.read_feather(eeg_arrow_data)",
    repeat=runs,
    number=evals,
    globals=globals(),
)
print("--------------")
print("Mean time: %.5f s" % (sum(stats) / runs))
print("Max time: %.5f s" % max(stats))
print("Min time: %.5f s" % min(stats))
print("--------------")
print("Samples: {}".format(runs))
print("Evals/Sample: {}".format(evals))
```

```
Total allocations: 14117.9 KiB
--------------
Mean time: 0.00415 s
Max time: 0.01197 s
Min time: 0.00340 s
--------------
Samples: 10000
Evals/Sample: 1
```

```python
from julia.api import Julia
import tracemalloc
from timeit import repeat

def pyjulia_alloc(fpath):
    tracemalloc.start()
    Arrow.Table(eeg_arrow_data)
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

jl = Julia(compiled_modules=False)
from julia import Arrow

eeg_arrow_data = "/home/src/Projects/neuriviz/data/exp_pro/sub-002/ses-01/eeg/sub-002_ses-01_task-gonogo_run-01_eeg.arrow"

runs = 10000
evals = 1
pyjulia_alloc(eeg_arrow_data)

stats = repeat(stmt="Arrow.Table(eeg_arrow_data)", repeat=runs, number = evals, globals=globals())
print("--------------")
print("Mean time: %.5f s" % (sum(stats) / runs))
print("Max time: %.5f s" % max(stats))
print("Min time: %.5f s" % min(stats))
print("--------------")
print("Samples: {}".format(runs))
print("Evals/Sample: {}".format(evals))
```

```
Total allocations: 0.9 KiB
--------------
Mean time: 0.00052 s
Max time: 0.05144 s
Min time: 0.00046 s
--------------
Samples: 10000
Evals/Sample: 1
```

```
Total allocations: 105738.9 KiB
--------------
Mean time: 7.42305 s
Max time: 7.83712 s
Min time: 7.21004 s
--------------
Samples: 10
Evals/Sample: 1
```


