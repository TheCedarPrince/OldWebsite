---
title: "Implementing Marching Squares"
image:
  path: /assets/squares_banner.png
comments: true
share: true
tags:
    - julia
    - algorithms
    - topography
---

_Naive Implementation of the Marching Algorithm for topography and 2D Graphics!_
{: .notice}
{: style="text-align: center;"}

One day, I was examining topoplots created from popular libraries like MATLAB's [EEGLAB](https://sccn.ucsd.edu/eeglab/index.php) and Python's [MNE](https://mne.tools/stable/index.html#) program for processing and visualizing EEG data.
I think the plots are beautiful and can be quite informative as shown from [Mikołaj Magnuski's example in MNE-Python](https://mne.tools/stable/auto_examples/visualization/plot_eeglab_head_sphere.html?highlight=topoplot):

![](/assets/mne_eeglab_topoplots.png)
{: style="text-align: center;"}

However, what was curious to me was how to make the boundaries one can see in the above image between the different color gradients.
I chatted with my friend and fellow programmer [Ole Kröger](https://opensourc.es/about/) about this and he explained this was accomplished via an algorithm called [Marching Squares](https://www.wikiwand.com/en/Marching_squares).
So, naturally, I had to figure out how to implement this for myself!

This algorithm is also used in providing 

![](/assets/topoplot_osm.png)
{: style="text-align: center;"}

# What Is the Marching Squares Algorithm?

A simplified explanation of the marching squares algorithm is that it can be thought of as a way of visually separating data based on a user defined threshold.
This data takes the form of a 2D array and the threshold (or _isovalue_ as it is generally termed) is used to filter each value in this array to either a $$0$$ if it does not reach the threshold or $$1$$ if it meets or exceeds the threshold.
Each $$2 \times 2$$ square in the provided grid creates a cell that will be used for creating the boundaries around thresholded values.

Following this simple explanation, lets get to implementing the algorithm!

# Implementing Marching Squares!

## All I See Are :one:'s and :zero:'s!

To start, we need some data!
I went ahead and created this $$10 \times 10$$ grid that has a threshold applied to it to make it hold only $$1$$'s and $$0$$'s.
We will be using the following array of values in this post:

```julia
10 × 10 Array{Int64,2}:
 0  1  1  0  0  0  1  0  1  0
 0  1  1  0  1  0  0  1  0  0
 0  0  1  1  0  1  1  1  0  0
 0  0  0  1  1  0  1  1  1  0
 0  0  1  0  0  1  0  1  0  0
 0  0  1  1  1  1  0  1  1  0
 0  0  0  1  0  0  1  0  0  0
 1  1  1  0  0  1  0  0  0  0
 0  0  1  0  0  1  1  1  0  1
 0  1  1  0  1  1  0  0  0  1
```

## Visualizing a Grid Using `Luxor.jl` :beetle:

To process this information and implement the algorithm, we need a way to actually visualize these values.
Thankfully, fellow Julia developer, [Cormullion](https://cormullion.github.io/), created a wonderful visualization library called [Luxor.jl](https://github.com/JuliaGraphics/Luxor.jl) that allows us to do just that!
One can add `Luxor.jl` to your Julia REPL by typing `]add Luxor`.
After that, let's start with making our script!

First, let's use Luxor and create a function that defines our background:

```julia
using Luxor

function make_drawing(width, height, img_path, bkg_color, origin_p)
    d = Drawing(width, height, img_path)
    background(bkg_color)
    origin(Point(0, 0))
    return d
end
```

`make_drawing` creates a `Drawing` object that we will then draw our future lines and shapes!
It requires you to specify the dimensions of your drawing, where to save the image, the background color, and an origin.
Upon execution, it gives you back the `Drawing` object ready for additional shapes to be drawn on it.

> **NOTE: What is an "origin" in `Luxor`?** 
>
> By default, `Luxor` assumes you want to draw everything based off the center of the `Drawing`'s given dimensions.
> To change the origin, we supply a `Point` from `Luxor` to `Luxor`'s function, `origin`.

Perfect!
Now that we have our drawing created, let's get to work actually showing our values.

I think the best way is to show zero's as white balls and one's as black balls.
To do this, let's create another function for our script:

```julia 
function draw_balls(drawing, grid)
    nrows, ncols = size(grid)
    step_x = drawing.width / (ncols - 1)
    step_y = drawing.height / (nrows - 1)
    circ_scale = min(nrows, ncols) / max(nrows, ncols)
    points = Array{NamedTuple}(undef, nrows, ncols)
    for i = 1:nrows
        for j = 1:ncols
	    grid[i, j] == 0 ? sethue("white") : sethue("black")
            pos = Point(step_x * (j - 1), step_y * (i - 1))
            circle(pos, 7.5 * circ_scale, :fill)
	    points[i, j] = (x = pos.x, y = pos.y, val = grid[i, j])
        end
    end
    return points
end
```

There is a lot happening in this new function! Let's examine the `draw_balls` function step by step to understand it:

1. The function takes in a `Drawing` object and the binary valued grid.
2. The number of rows and columns are determined from the grid.
3. `step_x` and `step_y` are calculated to find how much space should be between each ball along the `x` and `y` axes. (We subtract one away from the denominator of the step calculations to draw along the edges of the `Drawing`).
4. We create a scaling value, `circ_scale`, that scales our balls to an appropriate radius for the grid.
5. 




![](/assets/grid_squares.png)
{: style="text-align: center;"}

From there, we determine specific cases based on the smaller squares formed inside the previous grid (each of the four points).
More on this here: https://wikiwand.com/en/Marching_squares#/Basic_algorithm

I determine the case and associate each square with the case value.

![](/assets/square_markers.png)
{: style="text-align: center;"}

![](/assets/square_cases.png)
{: style="text-align: center;"}

asdfa

![](/assets/numbering_squares.png)
{: style="text-align: center;"}

Now, we need to determine how to draw the lines!
We have the case numbers, but how do we actually #plot the lines? 
For this, I calculate the cardinal locations in each square: north, east, south, and west.

These are represented small circles on this plot!

![](/assets/cardinal_squares.png)
{: style="text-align: center;"}

Finally, we can draw the, lines, technically, isolines by connecting each of these cardinal locations based on each squares case!

This yields our boundaries around the white and black balls:

![](/assets/iso_lines_squares.png)
{: style="text-align: center;"}

![](/assets/squares.png)
{: style="text-align: center;"}

