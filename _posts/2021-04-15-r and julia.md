---
title: "Interoperability with Julia & R"
image:
  path: 
comments: true
share: true
tags:
    - julia
    - r
    - interoperability
---

_Interoperability with Julia & R to Extend OHDSI Research_
{: .notice}
{: style="text-align: center;"}

The other day I was exploring tooling available in the [OHDSI community](https://github.com/OHDSI).
For those who are not familiar, the Observational Health Data Sciences and Informatics - [aka OHDSI](https://ohdsi.org/) - community is an international open science research collective whose goal is to "bring out the value of health data through large-scale analytics."
It is an exciting group that has done research on a myriad of topics using data provided from electronic health records and claims data.
The key tools provided by OHDSI to query OHDSI datasets are largely written in the `R` programming language.

## What Is `R`?

`R` is a popular programming language amongst those involved in social science research and public health.
It is an interpreted language and features many great built-in tools; it is notable for being the originator of the concept of a "Data Frame" which is now almost ubiquitous!
Here is an example of what `R` code looks like:

```R
data <- sample(16)
mat <- matrix(data, 4)
print(mat)
```

```
     [,1] [,2] [,3] [,4]
[1,]    6   10   12   15
[2,]    2   13    5    3
[3,]    1    9   14   16
[4,]   11    4    8    7
```

The `<-` for variable assignment blew my mind at first!
I had never seen syntax like that before, but I have come to appreciate how there is only one way to read the assignment as opposed to an `=` operator.

Before we leave this section doing a high level and fast exploration of `R`, 
something that I wanted to mention was this quote by Hadley Wickham, Chief Scientist in the team behind the popular "RStudio" tool, in his book _Advanced R (Second Edition)_:

> [...] `R` is not a fast language.
This is not an accident: `R` was purposely designed to make interactive data analysis easier for humans, not to make computers as fast as possible.
While `R` is slow compared to other programming languages, for most purposes, it’s fast enough.

This quote does not, in any way, speak ill about `R` or `R` programmers but rather, just lists a very real limitation of the language.
`R` has a rich ecosystem and toolchain that it would be a shame to discredit or avoid the language because of this limitation.
Now that you know a bit about `R`, how its syntax looks, and a little about its limitations, we can move onto the most exciting aspect of this blog: using `Julia` to execute `R` code!

## Why Use `Julia` To Execute `R` Code?

Aside from `Julia` being probably the best language I have ever used in my life, unlike `R`, it was built with speed, efficiency, and ease of use in mind.
There has been much written about `Julia` and I will not cover it all in this blog post [^1].
However, to illustrate that point, let's do a quick comparison regarding speeds of `Julia` and `R`.
The table comparing these benchmarks can be found [here]() - feel free to skip to it if you don't care too much about what exactly is happening with the benchmarks!
<!--TODO: add link here to multiple documents on Julia-->

### Light Benchmarking of `R`

At the suggestion of both Hadley Wickham and members of the `R` Discord community [discoRd](https://discord.gg/FQp6ZNd), I used the benchmarking library [`bench`](https://github.com/r-lib/bench).
For this benchmarking, all I am going to do is evaluate a few common use cases that come to my mind.

> For the sake of reproducibility if you want to try these benchmarks yourself, here is the `R` version and `bench` version. 
>
> ```
> print(R.version.string)
> [1] "R version 4.0.5 (2021-03-31)"
>
> print(packageVersion('bench'))
> [1] ‘1.1.1’
> ``````
>

Now for some `R` snippets with a brief explanation of what is happening with the benchmarks:

#### `R` Benchmark 1

```R
# Benchmark 1:
# Benchmarking creation of a 10 x 10 matrix of random float values
# from a normalized distribution.

library('bench') # Loading in the `bench` library

bench::mark(matrix(rnorm(100), nrow = 10, ncol = 10))
```

#### `R` Benchmark 2

```R
# Benchmark 2:
# Summing across the columns of a 10 x 10 matrix of random float values and 
# calculating the mean of the sums.

library('bench') # Loading in the `bench` library

mat <- matrix(rnorm(100), nrow = 10, ncol = 10)
bench::mark(mean(colSums(mat)), iterations = 10000)
```

#### `R` Benchmark 3

```R
# Benchmark 3:
# Substituting a substring in a long string for another substring.

library('bench') # Loading in the `bench` library

dummy_string <- "foobazbar"
bench::mark(sub("baz", "boo", dummy_string, fixed = TRUE), iterations = 10000)
``````

### Light Benchmarking of `Julia`

For `Julia`, I am using the [`BenchmarkTools`](https://github.com/JuliaCI/BenchmarkTools.jl) package which is the de-facto benchmarking toolkit in `Julia`.

> For the sake of reproducibility if you want to try these benchmarks yourself, here is the `Julia` version and `BenchmarkTools` version. 
>
> ```julia
> using Pkg # Needed to print version info of BenchmarkTools
>
> versioninfo()
>
> Julia Version 1.6.0
> Commit f9720dc2eb (2021-03-24 12:55 UTC)
> Platform Info:
>   OS: Linux (x86_64-pc-linux-gnu)
>   CPU: Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz
>   WORD_SIZE: 64
>   LIBM: libopenlibm
>   LLVM: libLLVM-11.0.1 (ORCJIT, skylake)
> Environment:
>   JULIA_EDITOR = nvim
>
> Pkg.status("BenchmarkTools")
> 
>       Status `~/.julia/environments/v1.6/Project.toml`
>   [6e4b80f9] BenchmarkTools v0.7.0
> ``````
>

Now for some `Julia` snippets with a brief explanation of what is happening with the benchmarks:

#### `Julia` Benchmark 1

```julia
# Benchmark 1:
# Benchmarking creation of a 10 x 10 matrix of random float values
# from a normalized distribution.

using BenchmarkTools

@benchmark randn(10, 10)
```

#### `Julia` Benchmark 2

```julia
# Benchmark 2:
# Summing across the columns of a 10 x 10 matrix of random float values and 
# calculating the mean of the sums.

using BenchmarkTools

mat = randn(10, 10)
@benchmark sum($mat, dims = 1) |> mean
```

#### `Julia` Benchmark 2

```julia
# Benchmark 3:
# Substituting a substring in a long string for another substring.

using BenchmarkTools

dummy_string = "foobazbar"
@benchmark replace($dummy_string, "baz" => "boo")
```

### Comparing Benchmarks between `R` and `Julia`

Using our above benchmarks, we can now do a loose comparison between these two great languages:

| Benchmark Number | Language | Min Time | Median Time | Iterations |
|------------------|----------|----------|-------------|------------|
| 1                | `R`      | 7220ns   | 16000ns     | 9999       |
| 1                | `Julia`  | 324ns    | 916ns       | 10000      |
| 2                | `R`      | 6190ns   | 21100ns     | 9998       |
| 2                | `Julia`  | 92ns     | 243ns       | 10000      |
| 3                | `R`      | 1300ns   | 2340ns      | 10000      |
| 3                | `Julia`  | 188ns    | 651ns       | 10000      |

> **NOTE:** Please note, this is not a rigorous exploration of benchmarking these two languages, but rather a quick comparison.

As you can see, `Julia` far outpaces `R` in all these benchmarks.
This makes sense as `Julia` is a compiled language - not interpreted like `R`.
I won't go into much detail about these differences here, but I wanted to give a feel for how fast `Julia` is - and moreover, why `R` users would want to leverage it [^4]!
<!--TODO: add footnote on further reading!-->

## Leveraging `Julia` To Call `R`!

If the benchmarks have convinced you, then let's get into calling `R` from `Julia`!
To follow along with what we are doing here, you must have `R` and `Julia` installed on your computer [^1].

First, we need to add the package, [`RCall`](https://github.com/JuliaInterop/RCall.jl), into `Julia`!
To do this, execute the following code block in your `Julia` REPL:

```julia
using Pkg
Pkg.add("RCall")
```

Now that `RCall` is installed, let's make sure that it works!
We can check this by running the following:

```julia
using RCall
```

> **NOTE:** If you run into issues with this step, please visit the [installation section of `RCall`](https://juliainterop.github.io/RCall.jl/stable/installation/).

And then press the `$` sign in your REPL!
You should get a new prompt that starts with `R>`.
What is this you might be wondering?
You are now accessing the `R` REPL from the `Julia` REPL!
Here is how that looks with a few different `R` commands having run:

![](/assets/julia_rcall.png)

### Case Study: OHDSI `R` Tools

The [Observational Health Data Sciences and Informatics](https://ohdsi.org/) program is an open science initiative focused on arming health scientists with the tools to perform large scale analytics on healthcare data.
They have a [wonderful toolchain](https://github.com/OHDSI) but, at the time of this writing, the tools are almost all exclusively written in `R`.
To ordinary programmers, this might seem like roadblock, but for us, `Julia` can build bridges for us to call these tools!

First, we need to install a package called [OMOPCommonDataModel.jl](https://github.com/JuliaHealth/OMOPCommonDataModel.jl).
We won't get too much into what the [OMOP Common Data Model](https://ohdsi.github.io/CommonDataModel/) actually is but in a nutshell, it is a way of standardizing unstructured healthcare data.
With the package, `OMOPCommonDataModel.jl`, we actually have an implementation in the language of this specification to structure healthcare type data!
We can add it to our `Julia` installation by using the command:

```julia
using Pkg
Pkg.add("OMOPCommonDataModel.jl")
```

And then we can use this package alongside `RCall`:

```julia
using RCall
using OMOPCommonDataModel
```

Perfect! Moving on from there, you can also go ahead and install the following packages in `R` with the following commands in an `R` REPL:

```R
install.packages(c("SqlRender", "DatabaseConnector", "remotes"))
remotes::install_github("ohdsi/Eunomia", ref = "v1.0.0")
```

To briefly summarize what these packages are, they are packages from the OHDSI community which allows us to get something very exciting: artificial healthcare data structured in the OMOP Common Data Model!
Since healthcare data in the United States falls under the protection of policies such as [HIPAA](https://www.hhs.gov/hipaa/index.html), it is not often easy to get access to healthcare data.
Much less healthcare data you can publicly share and analyze (for example: in a blog post!).
So the fact that OHDSI provides this data is fantastic for us!

Now that you have these packages installed in `Julia` and `R` we can now get to the exciting bit: calling `R` code from `Julia`!
We will be using the following `R` snippet:

```R
library('DatabaseConnector')
connectionDetails <- Eunomia::getEunomiaConnectionDetails()
connection <- connect(connectionDetails)

sql <-	"
	SELECT * 
	FROM @cdm.person
	LIMIT 1;
	"
result <- renderTranslateQuerySql(connection, sql, cdm ="main")
```

What this `R` snippet does, is it connects to OHDSI's artificial healthcare database called [`Eunomia`](https://github.com/OHDSI/Eunomia) (by the way, the OHDSI loves Greek names - [Eunomia is the goddess of law and legislation](https://www.wikiwand.com/en/Eunomia)!) that was installed on your computer when the `R` `Eunomia` package was installed.
It finds a person object from this database and returns it back to via an embedded SQL command - so I guess we are actually to use three languages in this example. :boom:
However, we are not going to run this code in `R`!
No! We will use `Julia` to do this; copy the next snippet into a file called `omop.jl`:

```julia
using RCall
using OMOPCommonDataModel

person = R"""
library('DatabaseConnector')
connectionDetails <- Eunomia::getEunomiaConnectionDetails()
connection <- connect(connectionDetails)

sql <-	"
	SELECT * 
	FROM @cdm.person
	LIMIT 1
	"
result <- renderTranslateQuerySql(connection, sql, cdm ="main")
""" |> rcopy

omop_person = [Person(vec(convert(Array, row))...) for row in eachrow(people)]
```

and then run it from the `Julia` REPL by doing the following:

```julia
include("omop.jl")
```

From R to Julia object:

```julia
@benchmark rcopy($person)
```

```
BenchmarkTools.Trial:
  memory estimate:  29.36 KiB
  allocs estimate:  532
  --------------
  minimum time:     66.786 μs (0.00% GC)
  median time:      153.143 μs (0.00% GC)
  mean time:        186.888 μs (7.75% GC)
  maximum time:     29.817 ms (98.23% GC)
  --------------
  samples:          10000
  evals/sample:     1

```

From Julia to R object:

```julia
@benchmark robject($julia_obj)
```

```
BenchmarkTools.Trial:
  memory estimate:  3.36 KiB
  allocs estimate:  92
  --------------
  minimum time:     6.007 μs (0.00% GC)
  median time:      15.137 μs (0.00% GC)
  mean time:        20.855 μs (8.84% GC)
  maximum time:     9.022 ms (81.01% GC)
  --------------
  samples:          10000
  evals/sample:     5
```

```R
install.packages("bench")
library(bench)

bench::mark(result[1, "PERSON_ID"])
```

| expression               | min   | median | `itr/sec` | mem_alloc | `gc/sec` | n_itr | n_gc |
|--------------------------|-------|--------|-----------|-----------|----------|-------|------|-------|
| `result[1, "PERSON_ID"]` | 8.5µs | 22.9µs | 39710.    | NA        | 7.94     | 9998  | 2    | 252ms |


