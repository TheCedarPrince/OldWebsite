## **Timing Scripts**

TheCedarPrince  2 hours ago
What is best practice for timing a Julia script post-JIT compilation? I have been doing:

```julia
using Dates
time1 = now()
# Code
# .
# .
println(now() - time1)
```

**David Varela**  2 hours ago
Use BenchmarkTools: https://github.com/JuliaCI/BenchmarkTools.jl


**Martijn Visser**  23 minutes ago
Note that BenchmarkTools runs your code multiple times to get an accurate benchmark. For a quick estimate see also `@time` which is in Julia Base: https://docs.julialang.org/en/latest/base/base/#Base.@time

**Mason Protter** 4:05 PM
Just do using BenchmarkTools and then
`@btime f()` to benchmark some function call

Just curious, why is my method poor?


**Roger Critchlow**  9 minutes ago
Simple timings tend to confound compilation time with execution time and they often miss the garbage collection penalty which only hits when enough garbage has been generated.  So BenchmarkTools.jl arranges to get the compilation done first and then times enough repetitions of the code to get a good estimate of execution times and costs.  Compilation time can involve recompiling lots of libraries to specialize for the types you throw at them.

## **Optimization**


**Eric Hanson**  22 hours ago
https://docs.julialang.org/en/v1/manual/performance-tips/ has lots of good tips in case you haven't seen it

## **Julia FAQs**

**Logan Kilpatrick**

1) one of the coolest parts of Julia is that there’s a community if people that are here to help outside of your research and work
I have a team at NASA but also a huge group of other Julia users who know little about what I do at NASA but are always willing to help. This is something you don’t see in other communities
2) one of the benefits of Julia is that it’s so fast you don’t need need to mix languages
Pure Julia should do the job.
Though im not sure that answered your question so feel free to ask it again if need be
Yesterday, 1:44 PM
3) the GR() backend is the fastest time to first plot. This issue arises because the original author of plots didn’t make things the right type. This has been improved significantly in the last couple of months
4) I use Julia 1.3 currently in Atom and also have the terminal version for quick tests
On top of that, I run Julia Pro for my work with JuliaComputing because that is the only way to get licensed software.
Yesterday, 1:46 PM
5) speed kills. If you watch the 2017 Julia con talk by prof Mykel kerkendurfer(I spelled that wrong 100%), I think he mentions there or in another paper that it saved the FAA like 100,000 years of computing time use Julia. Mykel subsequently advised my manager at NASA for his PhD at Stanford and helped write the Pomdps module that we use
And no worries! Always happy to chat. Feel free to ping me if you have other questions or follows

TheCedarPrince Today at 6:42 PM
I could not find an answer exactly to my question on the web: if I were to use Julia for a job, would I have to pay for it? Or is it free?
19 replies

**Mosè Giordano**:palm_tree:  8 minutes ago
pay for what?

TheCedarPrince  7 minutes ago
Pay for usage of the language - like a license or something else.

**caseykneale**  7 minutes ago
its free...

caseykneale  7 minutes ago
but you can buy stuff from julia lang

caseykneale  6 minutes ago
like juliapro or whatever

Mosè Giordano:palm_tree:  6 minutes ago
the main (and so far only) implementation of the language is free and open source.  there are some packages that are licensed (like some of the packages developed by Julia Computing :juliacomputing:), but the vast majority are free and open source as well (edited) 

TheCedarPrince  6 minutes ago
Hmmm... I guess my biggest point of confusion is why anyone would want to pay for JuliaPro - seems somewhat moot with the open source community and active development.

caseykneale  6 minutes ago
I actually looked into it

caseykneale  5 minutes ago
they offer some nice stuff, like you can pick packages by their licenses(so you can select ONLY MIT)

caseykneale  5 minutes ago
they also offer services around network barriers and things IT loves to set up

caseykneale  5 minutes ago
also, it's a nice thing to do and I doubt it's expensive. If I can get my new company on board, we'll pay julia pro

caseykneale  5 minutes ago
also they will help you out... and they are the people who know the language best

TheCedarPrince  2 minutes ago
Ah - this all makes sense. Thanks for the elucidation @caseykneale. :slightly_smiling_face:

caseykneale  1 minute ago
for sure, I mean I'm not expert, but it seems nice and again I doubt its expensive

caseykneale  1 minute ago
considering our company forks over like 2k a pop for shit 3rd party licenses

caseykneale  1 minute ago
much rather have support(bureacrasy loves that word)

TheCedarPrince  1 minute ago
Exactly, plus, the support you can get will a boon to other potential adopters who are reluctant to self-learn a new language.

caseykneale  < 1 minute ago
exactly

## **Plotting and Animations**

**Julius Krumbiegel**  14 hours ago

If you want to try it out, there is a library called Makie (I'm working on MakieLayout) which can be really nice for animations, as it plots via the GPU and uses Observables, which make updating plots for animations really simple.
I've quickly tried something like your example, you don't have to go through the trouble of saving all these frames out and combining them later. The whole thing is done in like 5 seconds on my machine, only the animation part without saving frames is 0.4 seconds:

(only precompiling everything for the first run is pretty slow)

## **Articles on Julia**

1. https://www.nature.com/articles/d41586-019-02310-3

## **Julia Workflow**

TheCedarPrince  4 hours ago
I am honestly not sure how the workflow is supposed to work in Julia (coming from Python land where testing scripts was a matter of python do_your_thing.py and I am realizing that is rather slow in Julia...). (edited) 

Spencer Russell  4 hours ago
PackageCompiler is more for compiling packages that you use but that don’t change very much. It’s not something you’ll generally use for code that you’re actively developing. I use Atom/Juno which is a nice combination of the file-editing workflow plus REPL-like live-execution
:+1:
2


**Spencer Russell**  4 hours ago
Also the JIT compiler isn’t something you invoke explicitly, it’s run every time you evaluate code

Mosè Giordano:palm_tree:  4 hours ago
Keep also in mind that Julia performance makes a difference in the long run. Running short scripts each in a fresh session is not going to be fun, because of the initial overhead (edited) 
:+1:
1


Sven-Erik Ekström  4 hours ago
if you develop small things wrap everything in functions and use include("foo.jl"). Then run the function. If you develop a package use Revise.jl (edited) 
:+1:
1


**Sven-Erik Ekström**  4 hours ago
that is at least how I do, might exist better ways :P

TheCedarPrince  4 hours ago
Exactly @mose and @ssfrr - I know it is part of the Julia toolchain but I guess I am more thinking of the live development idea. I actually just discovered Revise.jl  @sverek - freaking love it! Surprised it is not more advertised as it is amazing in my opinion.

**Brenhin Keller**  4 hours ago
I find it useful to have one repl per project (one Juno window really) and keep that open all the time lisp-style, restarting as infrequently as possible. Many people use Revise.jl to avoid having to restart the repl.

TheCedarPrince  4 hours ago
I am sincerely thinking about setting up Juno but it just feels weird that I need to get a new editor set-up to use just one language. I have been using VSCode for my dev and writing purposes, but I find the Julia package not to be as robust as I might hope (no offense to the VSCode Julia team!) since I tend to switch between multiple languages and tasks each day.

TheCedarPrince  4 hours ago
That is what I found myself doing @Brenhin Keller . I combo that method with also Revise.jl

TheCedarPrince  4 hours ago
I like that idea @sverek - I will incorporate that into my workflow. Thank you!
:+1:
1


TheCedarPrince  3 hours ago
And you are right @mose - when I finally figured out the proper toolchain, I was, and rightfully so, BLOWN AWAY by the speed.

**Spencer Russell**  3 hours ago
Yeah, I get the hesitance to use a new editor just for Julia, but IMO it’s slick enough to be worth it even if you do think of it as a Julia-specific IDE
:+1:
1


TheCedarPrince  3 hours ago
Hunh - I take you at your word @ssfrr! I shall try it out, but I am glad you see what I mean. If Juno was ported to VSCode, then that would be amazing!

**Miles Lucas**:star:  3 hours ago
@TheCedarPrince the VS Code julia extension works just as well. You open up a julia terminal and it’s already set to your local environment, then you can run tests and include stuff all you want. The trick is to put using Revise in your .julia/config/startup.jl file. #vscode has some more insight.
:+1:
1


TheCedarPrince  3 hours ago
Ah gotcha - it kept blowing up whenever I tried to use Julia 1.3.0 so I deemed it unreliable. I will check it out again.

TheCedarPrince  3 hours ago
Thanks @mileslucas

## **Initial Twitter Thoughts**

Happy Holidays Folks! 🎄

While I have been with family, I took some time to learn about the 
@JuliaLanguage
 from 
@MIT
.

This gif is of a dense matrix (y = 1's, p = 0's); I generated it via #python and #JuliaLang.

At first, I thought julia was a very odd language. Then, I got it.
4:47 AM · Dec 27, 2019·Twitter Web App
View Tweet activity
 Retweets
 Likes
JacobZelko
@Jacob_Zelko
·
Dec 27
Replying to 
@Jacob_Zelko
Julia is not trying to overthrow Python (just yet 😉), instead it directly leverages Python.

I made use of matplotlib and numpy from Python using 
@anacondainc
's environment, Julia's PyPlot and PyCall packages and made a frankenstein-esque script to make my gif.
JacobZelko
@Jacob_Zelko
·
Dec 27
Getting used to some of Julia's idiosyncrasies and how it handles computer science foundations was an adjustment.

I am iffy on code mixing and versioning (pythonistas, eat your heart out).

Then, when I got my first #visualization to work, the magic of julia hit me.
JacobZelko
@Jacob_Zelko
·
Dec 27
I could truly leverage the power of python in the context of julia without too much of a performance hit. When I realized that, the possibilities here are truly ENDLESS.

Some important points of feedback so far for the 
@JuliaLanguage
 team (as a layman):
JacobZelko
@Jacob_Zelko
·
Dec 27
1. There needs to be better julia+python management. Python's package management is challenging; julia's, is not. These two systems must remain distinct - Conda.jl is a great start (problems: why the base conda env, etc.). This makes debugging python+julia projects easier.
JacobZelko
@Jacob_Zelko
·
Dec 27
2. Better integration between julia+other languages in terms of linting (i.e. tooltips in editors like #code)

3. Style guide - projects could rapidly get confusing if you start mixing in other langs. I see nothing in the style guide about how to handle language mixing.
JacobZelko
@Jacob_Zelko
·
Dec 27
4. Loading in modules to julia from python conda envs takes a LONG time and is a big initial performance hit on my code - is there a reason for this?

Take this all with a grain of salt of someone doing a deep dive in julia for AI studies - as a layman.
JacobZelko
@Jacob_Zelko
·
Dec 27
I think the language has a great future and could really become one of the most extensible languages in the world - I see the vision for it and it  is great.

As a novice scientist and julia programmer, I hope to see that come to be. 🙂