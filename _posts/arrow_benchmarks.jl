using Arrow
using BenchmarkTools
using DataFrames

eeg_arrow_data = "/home/src/Projects/neuriviz/data/exp_pro/sub-002/ses-01/eeg/sub-002_ses-01_task-gonogo_run-01_eeg.arrow"

@benchmark Arrow.Table($eeg_arrow_data) |> DataFrame;
