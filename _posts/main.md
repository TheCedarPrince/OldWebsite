<!------->
<!--title: "NeuriViz (Part 1) - Performant Graphics for Neuroinformatics"-->
<!--image:-->
  <!--path: /assets/Taming Knowledge/library.jpg-->
  <!--caption: "Photo from [@alfonsmc10](https://unsplash.com/@alfonsmc10)"-->
<!--comments: true-->
<!--share: true-->
<!------->

I am quite excited to introduce a new side-project of mine called [`NeuriViz`](https://github.com/TheCedarPrince/NeuriViz)!
`NeuriViz` is a proof of concept application of the [`Javis.jl`](https://github.com/Wikunia/Javis.jl) package to create performant animated graphics and visualizations for a specific domain.
In this case, the domain of neuroinformatics! 

# How Did `NeuriViz` Come to Be?

[`NeuriViz`](https://github.com/TheCedarPrince/NeuriViz) started as an offshoot of my work on [`Javis.jl`](https://github.com/Wikunia/Javis.jl) that my friend, [Ole Kröger](https://opensourc.es/about/), and I created.
The `Javis` package acts as a general purpose library to easily construct informative, performant, and winsome animated graphics using the [Julia programming language](https://julialang.org/).
While working on `Javis`, I realized it had potential to be applied to domain specific graphics that can be difficult to make.
Given [my background in health sciences and cognitive disabilities](/about/), I used `Javis` to create an animation of a 10-20 EEG Electrode Array:

!!! ADD GIF HERE OF BRAIN FROM TUTORIAL 2 !!!

After I had created this, I reached out to a neuroscientist that I knew.
From there, I was connected with my collaborator on the project, Zachary Christensen.
Finally, after a few different conversations and back and forth, `NeuriViz` was created.

# Brain Topography of EEG Data 

Tremendous thank you to @Zachary Christensen for creating AxisIndices.jl and @quinnj for spearheading development on Arrow.jl (as well as answering some random questions that I have pertaining to Apache Arrow). I have spent the last week working on a ~10GB EEG dataset from openneuro.org (Go-nogo Categorization and Detection Task Dataset). Originally, this dataset was made specifically for the MATLAB tool, EEGLAB, but I was able to parse it to Julia readable input and convert the relevant data to .arrow binary files. From there, I did some very light benchmarking on reading and writing of Arrow files in conjunction with DataFrames.jl:
julia> using Arrow, BenchmarkTools, DataFrames, NeuriViz
julia> fdt_readable = fdt_parser(fdt_path, dims) |> permutedims |> DataFrame;
julia> println("$(size(fdt_readable)[1] * size(fdt_readable)[2]) values in this DataFrame.")
6399640 values in this DataFrame.
julia> @btime Arrow.write("eeg_data.arrow", fdt_readable);
  15.527 ms (1140 allocations: 104.30 KiB)
julia> @btime Arrow.Table("eeg_data.arrow") |> DataFrame;
  82.728 μs (1820 allocations: 106.42 KiB)
I thought this was immensely impressive and suitable for my use case of dealing with nearly ~2 billion data values. Further, the minimal allocations is quite nice and doesn't blow up my computer (I am sure some of my code here and methods could be improved, but I am already very pleased). After research and discussion, I think the implementation of Arrow.jl is very clean in that it natively handles memory mapping and allows me to work with "larger than memory" datasets.
After I got my data into .arrow formats came the complicated bit of finding a proper data structure to handle the information I had. The data was split across five different file formats and to find something that would allow me to handle time series data, tables, and miscellaneous information was complicated. Following much experimentation with tools such as AxisArrays.jl, NamedArrays.jl, and RecursiveArrayTools.jl, I tested AxisIndices and it was perfect for my use case (the other packages are great by the way - I am not sure if I explored them properly enough but I could not make them meet my need). When I constructed a data structure based off of AxisIndices.jl, I decided to do some light benchmarking as well on loading all my eeg data into an AxisArray:
julia> @btime load_eeg_data();
  142.191 μs (2444 allocations: 149.77 KiB)
Finally, the data structure that I was able to produce is so beautiful and simple to use. Dare I say, the accessing of the data structure may even be self-explaining as code. Please see the attached photo so you can see what I mean! Apologies for the long post but I was shocked at how amazing this entire process was. Kudos for the great and important work (also thanks for @turingtest37, @Oscar Smith, @chrisrackauckas , and @christopher-dG for additional help with me trying to figure this all out).
