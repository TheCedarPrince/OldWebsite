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

<blockquote class="twitter-tweet" data-dnt="true" data-theme="dark"><p lang="en" dir="ltr">Happy Holidays Folks! 🎄<br><br>While I have been with family, I took some time to learn about the <a href="https://twitter.com/JuliaLanguage?ref_src=twsrc%5Etfw">@JuliaLanguage</a> from <a href="https://twitter.com/MIT?ref_src=twsrc%5Etfw">@MIT</a>.<br><br>This gif is of a dense matrix (y = 1&#39;s, p = 0&#39;s); I generated it via <a href="https://twitter.com/hashtag/python?src=hash&amp;ref_src=twsrc%5Etfw">#python</a> and <a href="https://twitter.com/hashtag/JuliaLang?src=hash&amp;ref_src=twsrc%5Etfw">#JuliaLang</a>.<br><br>At first, I thought julia was a very odd language. Then, I got it. <a href="https://t.co/7L36z9wBfM">pic.twitter.com/7L36z9wBfM</a></p>&mdash; JacobZelko (@Jacob_Zelko) <a href="https://twitter.com/Jacob_Zelko/status/1210497355574894592?ref_src=twsrc%5Etfw">December 27, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

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

## Working on Julia in Teams

Question for the Julia community: what has it been like working on a Julia project on a team? With Python, we have standards such as PEP-8 and formatters/linters to use (such as Black, flake, pylama, etc.) which helps with communicating coded ideas, but how does it go with Julia? Could anyone speak to their experiences? And if you did work with Julia as a team, how did you make sure communication was clear and effective (in terms of code)? Thank you!




19 replies

caseykneale  18 hours ago
I think the real difficulty for us wasn't specifically "oh no you didn't underscore/capitalize xyz"

caseykneale  18 hours ago
it was moreso the one guy would make these undocumented function stacks (he was a FP purist) and no one could erm excuse the lack of a political term "unfuck them" but him.

caseykneale  18 hours ago
so to me, it's more important people agree on a code style, and an architectural paradigm that can scale beyond a single persons brain

caseykneale  18 hours ago
I see PEP-8 as a hyper specific waste of time. Some of it is good, most of it is just the result of entropic drives for politics

caseykneale  18 hours ago
I had a manager not allow me to push a seriously needed fix for several days because I spelled diagonal wrong in the comments
:grimacing:
1


caseykneale  18 hours ago
all about balance

Nick:lion_face:  18 hours ago
I use Julia at work - almost our entire production system is Julia - and it's mostly great. 
In term of dev tools, people use a variety of different editors and the style guide we use is open source (https://github.com/invenia/BlueStyle) but we don't use linters or formatters, it's just an agreed convention (we may point to it in code review, but following a style has near enough removed style debate from code review)
I think some colleagues use Debugger.jl and maybe even MagneticReadHead.jl (the other debugger); but I don't know too much about other people's set-up. I use vim with Julia syntax highlighting but nothing else Julia specific  Anyway, I don't miss much from python development.
Oh, also the Test stdlib is nice and easy to use. We also use Memento.jl for logging (I think there are quite a few alternatives too) (edited) 
:+1:
2


caseykneale  17 hours ago
I assume you don't have anyone on your team refusing to use for-loops or any real form of built in loop structures in favor for weird functions that do the same thing? :slightly_smiling_face:

Nick:lion_face:  17 hours ago
Not yet! At least not in any code I've seen... so not in any code anyone else is expected to use. Thanks guess I should be grateful :smile:  
Gives me an excuse to mention something else really useful: BenchmarkTools.jl - so easy to benchmark code! (Although unfortunately writing a suite of benchmarks that runs on CI is not yet quite as nice an experience as writing tests) (edited) 
:smile:
1


oxinabox:ox:  17 hours ago
> refusing to use for-loops or any real form of built in loop structures in favor for weird functions that do the same thing?
@Nick, I feel like the first time I showed you mapreduce you would have disagreed (edited) 

Chris de Graaf  17 hours ago
Hahaha the "refuses to write for loops" thing sounds exactly like me
:laughing:
1


Nick:lion_face:  17 hours ago
Oh yeah maybe I didn't understand that comment afterall. (edited) 

oxinabox:ox:  17 hours ago
Something worth mentioning is how great the package manager is. Break your system into many packages, ability to release them separately knowing the package manager has your back to control what used what.
I wrote a thing on Discourse about that I while ago.
https://discourse.julialang.org/t/advice-on-structuring-larger-codebases/28203/17?u=oxinabox
I can't imagine working on a codebase with 4+ active projects running without the ability to break it down and manage it using releases.
JuliaLangJuliaLang
Advice on structuring larger codebases
Invenia has what is probably the largest closed source julia code base in existance. Last count was about 50 odd close source packages, and about the same open source (not counting ones that are primarily maintained by others). Invenias most significant application used over half of them (transitively), almost all of them are able to be also used for research projects also. E.g. to develop and test new algorithms. We have a private registry. The breaking up of things in to packages is gre...
Nov 9th, 2019
:100:
3
:+1:
1


Nick:lion_face:  17 hours ago
One thing I do appreciate is not having folks wanting to use macros or Cassette.jl when a function is perfectly adequate
:heavy_check_mark:
1


Nick:lion_face:  17 hours ago
Also we have a decent culture of documentation (but that's still an ongoing effort) - codebases with docstrings (and judicious comments) are much easier to maintain! I think that might make an even bigger difference than having a consistent style.
:juliadocs:
1
:speech_balloon:
1
:heart_eyes:
1


oxinabox:ox:  17 hours ago
An observation on formatters: once you have a team that has been consistently following a style guide for years, it's not as bad as you might think to keep it being followed.
I do miss having a linter.
In Julia 0.4, Lint.jl was really nice for catching things like unused variables, or other typos.
:+1:
2


oxinabox:ox:  17 hours ago
Not that I don't want a formatter though.
I think I saw that @domluna's formatter was getting YASGuide support.
BlueStyle support shouldn't be hard to add on top (since they are similar, with Blue being approx a more restrictive YAS) of we get some time. (edited) 

domluna  17 hours ago
Yeah I’m I have a experimental branch where I have this thing called “styles” aka multiple dispatch and it allows you to overwrite parts of the formatter. Using YAS as a proof of concept it works quite well so far. 
:heart:
3
:thankyou:
1


domluna  14 hours ago
bluestyle looks pretty similar to the current formatter, certain parts being more or less restrictive.




TheCedarPrince:deciduous_tree:  16:02
This isn't really a gripe, but is it just me or is finding the right Julia package for what you are trying to do very hard? I was beginning to create my own package when I discovered there were other small random packages that did what I wanted on GitHub somewhere. I guess I have been spoiled in Python where I could import scipy, sympy, matplotlib, numpy, or pandas and have basically everything I need right there. In Julia, it seems like packages are much more modularized and smaller - is that a good thing? Because it is leading me to get confused about where things are... It reminds me of a comment from @caseykneale about there being a problem with package advertisement in Julia. :stuck_out_tongue:
Not to just complain without a solution, but what is everyone's thoughts? As well as thoughts on perhaps making like an "Awesome JuliaLang" list on GitHub that lists out useful packages in specific categories?

mose  16:04
I think discoverability and modular packages are orthogonal problems
:+1:
5
:100:
4


asinghvi17  16:04
I think there are some metapackages in statistics and stuff, but that’s very much not the norm

David Varela  16:07
An "Awesome JuliaLang" does exist: https://github.com/svaksha/Julia.jl

ericphanson  16:09
There’s also https://pkg.julialang.org/docs/ and https://juliaobserver.com that can be helpful
juliaobserver.comjuliaobserver.com
Julia Observer
Julia Observer helps you find your next Julia package. It provides a visual interface for exploring Julia's open-source ecosystem.(214 kB)
http://d7edrf0ezfn0g.cloudfront.net/images/logo.png

1 reply
1 day agoView thread

Tom Kwong:dog:  16:12
 I guess I have been spoiled in Python where I could import scipy, sympy, matplotlib, numpy, or pandas and have basically everything I need right there
What would it be like if there's a meta package that bundles/re-exports the equivalent Julia packages?  One issue is that the precompilation time may be too long...
:heart:
1


TheCedarPrince:deciduous_tree:  16:17
Now THAT would be interesting @Tom Kwong - perhaps a way to handle the precompilation time is to do something like:
using Jundl # Julia Package Bundler = Jundl
jundl.dsp() # To compile only packages related to dsp tasks
I just remember that Plots.jl uses that idea of a backend and was wondering if we could leverage the same thing here.
16:17
Thoughts?

Tom Kwong:dog:  16:21
For the precompilation issue, maybe we can go the JuliaPro way and make it "batteries included" and fully charge the batteries ahead of time via PackageCompiler.  But then it would be a separate release train.
:point_up:
2

16:23
With the unreasonable effectiveness of multiple dispatch, it seems that package authors do need to get together and hash out common concepts and create easy to use APIs for general users.  The Tables.jl story is quite illuminating.  MLJ is also ambitious with its goals.

oxinabox:ox:  16:27
I think blog posts on sets  packages of packages is a good idea for discoverability. (They should also help with SEO of packages)
I did one on about 5 string related packages a while back
https://white.ucc.asn.au/2018/05/03/Strings-Types-in-Julia.html
And another about 7 binary classifier libraries even longer ago (that people still often read)
https://white.ucc.asn.au/2017/12/18/7-Binary-Classifier-Libraries-in-Julia.html
I think more people doing more of this would be great.

caseykneale:rubberduck:  16:29
thanks for the mention @TheCedarPrince but I'll be clear - I am part of the discoverability problem. My package is too many things in on box hehehe. But yea, I agree, a big list of "awesome julia" would be great. I am going to kickstart one but that isn't mine so if someone beats me to it I'd love to contribute!
16:30
basically we have a topic modelling problem, we can easily solve it with all the NLP'ers here :stuck_out_tongue:

oxinabox:ox:  16:30
One advantage of blog posts is they are a). Obviously personal opinions so less politics getting into it. (E.g. it's not generally ok for something in e.g. the manual to reference 1 package without mentioning it's competitors)
b) it a object in time.
Blogs generally have dates attached and are not expected to be updated.
So you can do it and forget -- no maintaince burden .
Can later post a follow up, if it takes ones fancy. (edited) 
:100:
6


caseykneale:rubberduck:  16:32
blogs are great things too :slightly_smiling_face:
16:33
what I want to make is a big living map of the julia ecosystem that's both queryable, explorable, and visual

Tom Kwong:dog:  16:36
Ideally, blogs can be more organized.  As a new Julia user, it would be nice to get to a place and pick what I want to explore e.g. machine learning, data wrangling, statistics, etc. and in no more than 3 clicks then I can get an idea what I can use.  Apparently the Apple web site is designed that way -> to lure you into buying their product :wink:

caseykneale:rubberduck:  16:37
I think we've hit kind of a rough spot though with some things. Some of the new users come in here like "So I am following tutorial X and the first line doesn't run" because things have changed so much
16:38
so it would be good to have something kind of curated as well
16:38
so people less aware of the Julia timescale can have a bit of a safetynet for whats new/old/etc

Zachary Christensen  16:39
The only automated way of doing this that I can think of is using GitHub tags

caseykneale:rubberduck:  16:39
yea or maybe a shared toml or something


3 replies
Last reply 1 day agoView thread

Zachary Christensen  16:41
If it takes any degree of curation you really end up needing experts for each domain of interest that volunteer to maintain a page

caseykneale:rubberduck:  16:42
hmm is it possible to put a change listener in a github page? Like set up a cronjob looking for major sem ver releases

caseykneale:rubberduck:  16:42
and if something changes throw a "note a new sem ver release was made" sorta thing


4 replies
Last reply 1 day agoView thread

oxinabox:ox:  16:42
Practically speaking new users need to learn about the Julia timescale.
Because there will always be lots of old resources.
As time moves forward there will be less as a proportion though.
As packages move to stability

caseykneale:rubberduck:  16:43
very true Lyndon

Zachary Christensen  16:44
There was discussion of package metrics on discourse a while ago.
16:45
If I know code coverage, number of commits, number of open issues, time since last commit, etc. I can usually get a good idea of where a package is at and worth using. (edited) 

caseykneale:rubberduck:  16:48
I try not to judge a package by those things because you never know. Something could just be stable and left alone.

Zachary Christensen  16:48
If a package is stable usually it has good coverage though.



5 replies
Last reply 1 day agoView thread

caseykneale:rubberduck:  16:49
true... reminds me I need to write more unit tests for mine :rolling_on_the_floor_laughing:

Zachary Christensen  16:51
For example. Every once in a while I see a package that was updating over a year ago but it's coverage is over 90% so maybe  they wouldn't need another commit unless there's some new feature implemented.

chrisrackauckas  16:53
I'm happy it's like this, because otherwise you have the other issue. Most of SciPy is pretty bad and not well-maintained, but it's big enough that people use it anyways. That's not a good situation to be in either.
:+1:
5

5 replies
Last reply 1 day agoView thread

chrisrackauckas  16:53
I think grouping in large enough orgs is the right middle ground.

Tom Kwong:dog:  17:12
replied to a thread:
yea or maybe a shared toml or something
This sounds like a good idea. I want to know what you have in your toml if I’m going to experiment some climate modeling. So I just instantiate and follow your guide (if you’ve written one). 
View newer replies

chrisrackauckas  17:38
replied to a thread:
I'm happy it's like this, because otherwise you have the other issue. Most of SciPy is pretty bad and not well-maintained, but it's big enough that people use it anyways. That's not a good situation to be in either.
well I think there's more too it. Too much in a scientific library is too much for anyone. No one is a master of all areas of numerical analysis. You stick too much stuff in there and soon you only have one master's student as the only person updating the ODE solvers once every few months.