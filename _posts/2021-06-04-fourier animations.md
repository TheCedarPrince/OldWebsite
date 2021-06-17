---
title: "Dancing with Ghosts: Animated Outlines"
image:
  path: /assets/squares_banner.png
comments: true
share: true
tags:
    - julia
    - javis
    - algorithms
    - signal processing
    - image processing
---

Several months ago, [Riccardo Cioffi](https://www.rcioffi.com/) contributed a fantastic example to the [`Javis` library](https://github.com/Wikunia/Javis.jl) which was using a Fourier tranform to draw image outlines using `Javis`.
In this case, the example was of drawing the Julia logo provided by the package, [`Luxor.jl`](https://github.com/JuliaGraphics/Luxor.jl).
Here is that animation:

![](assets/julia_logo_dft.gif)

It was an application of the Travelling Salesman Problem, a Fast Fourier Transform and the animation capabilities provided by `Javis`.
It occurred to me that this can be extended to any arbitrary image, and that is what this post focuses on!

# What all do we need to get this working?
For this we need mainly two concepts from mathematics viz., the Travelling Salesman Problem(TSP) and Descrete Fourier Transform (DFT). Apart from this, we would also need some basic imgage
processing to get the necessary boundary points from the image. Let us look at TSP and DFT in a little more detail.

## Travelling Salesman Problem
[Travelling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem) is a legendary problem posed by [William Rovan Hamilton](https://en.wikipedia.org/wiki/William_Rowan_Hamilton) (the same guy who formulated the hamiltonian mechanics, a true legend!) in the 1800s. The problem statement is: **Given a set of cities, what is the shortest route a salesman can take so that he visits each city once and returns to the city where he started from?**. This is an NP hard problem, meaning that the time taken to solve it does not increase polynomially with the input size. It increases exponentially. There are algorithms to solve TSP like Simulated annealing and Genetic Algorithms. However, description of those is outside the scope of this blog. In this case, we will use a convinient julia package [TravelingSalesmanHeuristics](https://github.com/evanfields/TravelingSalesmanHeuristics.jl) to solve this.

But why do we need TSP for this? By processing the image, we will get the coordinates of the points that form the border of the image. But those points are in a different order than what we desire. Look at it this way, we have a list of points on a 2D plane and we need to join them is such a way that the line does not cross each other and ends where it started. Sounds very similar to the TSP right? With this we will arrange the points in such a fashion that if we iterate through the arranged points, we would get the outline of the image in either clockwise sense or counter-clockwise sense (both are equally good!).

## Descrete Fourier Transform
Desrete Fourier transform is the the descrete analogue of the fourier transform. This [post](https://betterexplained.com/articles/an-interactive-guide-to-the-fourier-transform/)
describes DFT in a very beginner friendly manner. Going into a bit of a math, what DFT does is takes data in time domain and returns the data in the frequency domain. One place where fourier transform really shines is to approximate arbitrary functions. Consider that we have a function $f(t)$ which takes in a real number input `t` and returns a complex number, we wish to write this arbitrary function as sum like this:
 $$f(t) = \sum_{n} c_{n} e^{n * 2 \pi i t}$$ 

 Each term of the summation can be though of as a vector of length $|c_n|$ rotating with the frequency n units/sec. And thus, this sum can be though of adding such vecotrs according to vector addition and their rotation is governed by the individual frequencies. Given such a time evolution, the tip of the last arrow will trace out the arbitrary function in the complex plane (which for this purpose is equivalent to a 2D real plane). [3Blue1Brown's](https://www.youtube.com/watch?v=r6sGWTCMz2k) video on this is an excellent resource to see how this really works.

 What we get from image processing is the the coordinates of the boundary of the image and those coordinates are 2D coordinates so each point can be identified by a complex number in the [complex plane or the argand plane](https://en.wikipedia.org/wiki/Complex_plane) and we aim to trace out the border in the form af an animation. Sounds exactly what DFT can do right? For doing DFT, I will use an algorithm [Fast Fourier Transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform) which can be very conviniently used witht help of an awsome julia package [FFTW.jl](https://github.com/JuliaMath/FFTW.jl).

# Image Processing
We need to extract the extract the boundary of the object from the image. A very easy way to do this will be to first get a binary image where only the object boundary is white in color and the back ground is black and then apply thinning to skeletonize the image so that the boundary is only one pixel wide. All this can be very easily done by the package [Images.jl](https://github.com/JuliaImages/Images.jl).

Thining is a morphological operation(morphological operation is something that changes the morphology of the image). It esselntially squeezes all the objects (objects are the entities having pixel value one in the binary image) so that they are only one pixel wide.

To do so, we need to first convert the RGB image to gray scale image and then convert the grayscale image to a binary image. Then we can use the function `thinning` provided by `ImageMorphology.jl`.


The packages that we would be using to do the processing are,
```julia
using Colors: RGBA
using FileIO
using Images
using Luxor
```

Next, load the image using the `load` function. This will return an array with elements of the type `RGBA`. The image needs to in grayscale. For this, the function `Gray` from `Images.jl` can be broadcasted over the array.

```julia
img = load(File(format"PNG","person.png")) .|> Gray
```
This is how the image looks.

![](~/Documents/fft_animation/person.png)

Now, we have converted the RGB image to gray scale image. Now, we need the object to be white in color and the background to be black in color. What we have is opposite. Thus, the next step is to invert the image and then binarize it. To binarize the image, we need to threshold. From the image I could see that the black part is all zero and and the white part is non zero. Hence, 0 is a good threshold. So I set all the values above zero to 1 and all values equal to 0 as zero. These two tasks can be very conviniently combined into one line of code.

```julia
inv_img = 1 .- (img .> 0) .|> Bool
```
After inverting and then converting to binary, the image look like this.

![](~/Documents/fft_animation/person_inversion.jl)

Great. Now we have the object i.e., the persons oultline in white color (in binary it is 1) and the background as black. 

The `Bool` is needed in the end becuase the `thinning` function needs a boolean matrix as input.

Now that we have the boolean matrix, we can  skeletonize the image.

```julia
thin_img = thinning(inv_img)
```
with this we get,

![](~/Documents/fft_animation/person_thinned.png)

`thin_img` is the processed image from which we can extract out the points using a very simple function.

```julia
function get_points(img)
	findall(x -> x == 1,img) .|> x -> Point(x.I)
end
```

The function `get_points` takes the binary image as input and returns an array of points as formed by `Luxor.jl`

Now, we are all set for animating our man!

# Animating

For creating the animation we need a few packages.

```julia
using FFTView
using FFTW
using FileIO
using Images
using javis
using TravellingSalesmanHeuristics
```

Let us define some function that will be needed to draw the various shapes and objects involved in the animation. As we saw in the DFT section, we have to make a lot of circles and arrows not at the origin but at from the point where the previos arrow head was and also move them with different frequencies obtained by the FFT. It is best to define some functions so that drawing all that would become easier.

 ```julia
function ground(args...)
	background("black")
	sethue("white")
end

function my_arrow(start_pose, end_pose)
	arrow(
	start_pos,
	end_pose;
	linewidth = distance(start_pos,end_pos)
	arrowheadlength = 7,
	)
	return end_pose
end

function circ(;r = 10,vec = O, action = :stroke, color = "shite")
	sethue(color)
	circle(O,r,action)
	my_arrow(O,vec)
	return vec
end

function draw_line(
	p1 = O,
	p2 = O;
	color = "white"
	action = :stroke,
	adge = "solid"
	linewidth = 3,
	
)
	sethue(color)
	setdash(edge)
	setline(linewidth)
	line(p1, p2, action)
end

function draw_path!(path, pos, color)
	sethue(color)
	push!(path, pos)
	
	return draw_line.(path[2:end],path[1:(end - 1)]; color = color)
end

```



Since the FFT gives us a complex number as output, we need a function that will return the point that can be read by `Luxor.jl` and `Javis.jl`.

```julia
c2p(c::Complex) = Point(real(c),imag(c))
```

Before we go into the main function we need two more helper functions.

```julia
remap_idx(i::Int) = (-1)^i * floor(Int, i/2)
remap_inv(n::Int) = 2n * sign(n) - 1 * (n > 0)
```

<No idea what these functions are for>

Finally...we come to the main animation function.

```julia
function animate_fourier(options)
    #npoints = options.npoints
    nplay_frames = options.nplay_frames
    nruns = options.nruns
    nframes = nplay_frames + options.nend_frames

    # Obtain the points from the imeg
    points = get_points(load(File(format"PNG", "person_thinned.png")))
    npoints = length(points)
    println("#points: $npoints")
	
    # solve tsp to arrange the points
    distmat = [distance(points[i], points[j]) for i = 1:npoints, j = 1:npoints]

    path, cost = solve_tsp(distmat; quality_factor = options.tsp_quality_factor)
    println("TSP cost: $cost")
    points = points[path] # tsp saves the last point again

    # optain the fft result and scale
    y = [p.x - options.width for p in points] ./ 3
    x = [p.y - options.height for p in points] ./ 3

    fs = FFTView(fft(complex.(x, y)))
	 
    # normalize the points as fs isn't normalized
    fs ./= npoints
    npoints = length(fs)
	
	# make the animation
    video = Video(options.width, options.height)
    Background(1:nframes, ground)

    circles = Object[]

    for i = 1:npoints
        ridx = remap_idx(i)

        push!(circles, Object((args...) -> circ(; r = abs(fs[ridx]), vec = c2p(fs[ridx]))))

        if i > 1
            # translate to the tip of the vector of the previous circle
            act!(circles[i], Action(1:1, anim_translate(circles[i - 1])))
        end
        ridx = remap_idx(i)
        act!(circles[i], Action(1:nplay_frames, anim_rotate(0.0, ridx * 2π * nruns)))
    end

    trace_points = Point[]
    Object(1:nframes, (args...) -> draw_path!(trace_points, pos(circles[end]), "pink"))

    return render(video; pathname = joinpath(@__DIR__, options.filename))
    # return render(video; liveview = true)
end
```

Let's break this function and see what each chunk is doing.

1. The first chunk sets up the parameters we need to make the video. 
2. The second chunk is for getting the points from the iamge. I passed the thinned image that I got from the processing.
3. Third chunk is to solve the travelling salesman problem to arrange the points in a proper sense.
4. Fourth and the fifth chunk performes the fast fourier transform on the arranged points to get the necessary information. The fft is also normalised.
5. The last chunk is where the animation is made. Let us look at it in further detail.
   1) First the video is initialised with proper parameters and the background color is set.
   2) Then the `for` loop starts which creates the bunch of circles for each point which is stored in the array `circles`.
6. The last line returns the animation. If you want to see the animation frame by frame with a slider, then that can be very easily done by using the `liveview = true` option provided in `Javis.jl`. This line to do that is commented. Just uncomment that and comment to previous line to get that.

 <This part of Javis can be improved by a lot>
 
 Now we are all set to run this function and finally create out animation. Yayy!!
 
 This function `main` runs the function `animate_fourier` with the proper gif parameters
 
 The parameteres that are tunable are,
1. [`tsp_quality_factor`](https://evanfields.github.io/TravelingSalesmanHeuristics.jl/latest/index.html#TravelingSalesmanHeuristics.solve_tsp): This is the quality factor that denotes the trade off between the quality of solution and the computation time.
2. `width` and `height` are for the dimention of the gif.
3. `nruns`: This specifies how many times the path gets traced.
4.`nplay_frames` and `nend_frames` control the number of frames that would make up the gif and the number of frames to be inserted at the end of the gif respectively.

```julia
function main()

	gif_options = (
        # npoints = 1001, # rough number of points for the shape => number of circles
        nplay_frames = 600, # number of frames for the animation of fourier
        nruns = 1, # how often it's drawn
        nend_frames = 200,  # number of frames in the end
        width = 455,
        height = 490,
        tsp_quality_factor = 20,
        filename = "julia_fast.gif",
    )


    return animate_fourier(gif_options)
end
```
Running this function gives the animation that we wanted to see!

# Conclusion
This is a really cool application of `Javis.jl` to trace out the boundary of an arbitrary image. TO usm up the process, all you have to do to extend this to any arbirary curve is 
	1. Get the points either defining them yourself or by processing some image.
	2. pass the points to `animate_fourier` function
	3. Run the `main` function and voila you have the animation.

I hope this tutorial showed how extremly powerful fourier transform is and how easy is to make the animations in `Javis.jl`.

# Full Code

FInd the full working code used in the tutorial. Be sure to change the path of the image you want to give. And also, this processing is not universal and might vary image to image. Remember the end point of the processing is to obtain a binary image with the curve you want to trace and that curve should be one pixel thick.


```julia
# import packages
using Colors: RGBA
using FileIO
using Images
using Luxor


# Some helper functions
function ground(args...)
	background("black")
	sethue("white")
end

function my_arrow(start_pose, end_pose)
	arrow(
	start_pos,
	end_pose;
	linewidth = distance(start_pos,end_pos)
	arrowheadlength = 7,
	)
	return end_pose
end

function circ(;r = 10,vec = O, action = :stroke, color = "shite")
	sethue(color)
	circle(O,r,action)
	my_arrow(O,vec)
	return vec
end

function draw_line(
	p1 = O,
	p2 = O;
	color = "white"
	action = :stroke,
	adge = "solid"
	linewidth = 3,
	
)
	sethue(color)
	setdash(edge)
	setline(linewidth)
	line(p1, p2, action)
end

function draw_path!(path, pos, color)
	sethue(color)
	push!(path, pos)
	
	return draw_line.(path[2:end],path[1:(end - 1)]; color = color)
end

c2p(c::Complex) = Point(real(c),imag(c))

remap_idx(i::Int) = (-1)^i * floor(Int, i/2)
remap_inv(n::Int) = 2n * sign(n) - 1 * (n > 0)

# function to create the animation
function animate_fourier(options)
    #npoints = options.npoints
    nplay_frames = options.nplay_frames
    nruns = options.nruns
    nframes = nplay_frames + options.nend_frames

    # Obtain the points from the imeg
    points = get_points(load(File(format"PNG", "person_thinned.png")))
    npoints = length(points)
    println("#points: $npoints")
	
    # solve tsp to arrange the points
    distmat = [distance(points[i], points[j]) for i = 1:npoints, j = 1:npoints]

    path, cost = solve_tsp(distmat; quality_factor = options.tsp_quality_factor)
    println("TSP cost: $cost")
    points = points[path] # tsp saves the last point again

    # optain the fft result and scale
    y = [p.x - options.width for p in points] ./ 3
    x = [p.y - options.height for p in points] ./ 3

    fs = FFTView(fft(complex.(x, y)))
	 
    # normalize the points as fs isn't normalized
    fs ./= npoints
    npoints = length(fs)
	
	# make the animation
    video = Video(options.width, options.height)
    Background(1:nframes, ground)

    circles = Object[]

    for i = 1:npoints
        ridx = remap_idx(i)

        push!(circles, Object((args...) -> circ(; r = abs(fs[ridx]), vec = c2p(fs[ridx]))))

        if i > 1
            # translate to the tip of the vector of the previous circle
            act!(circles[i], Action(1:1, anim_translate(circles[i - 1])))
        end
        ridx = remap_idx(i)
        act!(circles[i], Action(1:nplay_frames, anim_rotate(0.0, ridx * 2π * nruns)))
    end

    trace_points = Point[]
    Object(1:nframes, (args...) -> draw_path!(trace_points, pos(circles[end]), "pink"))

    return render(video; pathname = joinpath(@__DIR__, options.filename))
    # return render(video; liveview = true)
end

# function to run the animation function
function main()

	gif_options = (
        # npoints = 1001, # rough number of points for the shape => number of circles
        nplay_frames = 600, # number of frames for the animation of fourier
        nruns = 1, # how often it's drawn
        nend_frames = 200,  # number of frames in the end
        width = 455,
        height = 490,
        tsp_quality_factor = 20,
        filename = "julia_fast.gif",
    )


    return animate_fourier(gif_options)
end
```

