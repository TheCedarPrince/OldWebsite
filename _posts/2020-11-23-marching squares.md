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

If you find this blog post useful, please consider citing it:

> Jacob Zelko. _Implementing Marching Squares_. December 1st, 2020. http://jacobzelko.com

# What Is the Marching Squares Algorithm?

A simplified explanation of the marching squares algorithm is that it can be thought of as a way of visually separating data based on a user defined threshold.
This data takes the form of a 2D array and the threshold is used to filter each value in this array to either a $$0$$ if it does not reach the threshold or $$1$$ if it meets or exceeds the threshold.
Each $$2 \times 2$$ square in the provided grid creates a cell that will be used for creating the boundaries around thresholded values.

Following this simplified explanation, lets get to implementing the algorithm!
I always find explanations easier to understand after seeing the full implementation. :smiley:

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

I think the best way is to show $$1$$'s as black balls and $$0$$'s as white balls.
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

There is a lot happening in this new function!
Let's examine the `draw_balls` function step by step to understand it.

First, there is a bit of initialization that occurs before we get to actually drawing the balls - let's start here!

1. The function takes in a `Drawing` object and the binary valued grid.
2. The number of rows and columns are determined from the grid.
3. `step_x` and `step_y` are calculated to find how much space should be between each ball along the `x` and `y` axes. (We subtract one away from the denominator of the step calculations to draw along the edges of the `Drawing`).
4. We create a scaling value, `circ_scale`, that scales our balls to an appropriate radius for the grid.
5. Finally, `points` is initialized to an array of `NamedTuple` objects that we will use to store the position and associated value of each ball.

Now that everything is initialized, let's get to drawing the balls!

1. We use two loops to access our grid to get the value for each ball we are going to draw and once we get the value from the grid, we use a ternary statement to `sethue` the color of our ball.
Remember, that the $$0$$'s are white and $$1$$'s are black!
2. Next, we determine the position of each circle by using the steps we calculated. 
Here, we subtract away $$1$$ from our indexing values so we are able to draw at the edges of our `Drawing`.
3. The `Luxor` function, `circle` is actually what we use to draw the balls!
This takes in the position of the circle we calculated in the last step and sets a radius based on our scaling factor.
`:fill` allows us to color in the circle to create a ball.
4. Finally, we store the x and y position of each ball, along with its value from the input grid, into our `points` array as a `NamedTuple`.
The `points` array is then returned to us for later usage.

Whew!
That was a lot of work!
However, it was worth it because now we get this nice layout of our balls:

![](/assets/grid_squares.png)
{: style="text-align: center;"}

Now that we have our layout, we are ready to implement our algorithm!

## In This Case... :briefcase:

If you look at our layout and how we drew it, all the points form the corners of rectangles.
With each of these rectangles, we can associate them with a value based on the values of the circles at each corner of these rectangles.
If that sounds confusing, here is a picture to better explain it:

![](/assets/square_markers.png)
{: style="text-align: center;"}

In this image, the balls here represent four balls taken from our grid.
Together, based on our layout, they form a rectangle.
In a clockwise fashion, starting from the top left of the rectangle, I label each corner, `a`, `b`, `c`, and `d` accordingly.
To assign a rectangle a value, we count the values at each corner as part of a 4 bit structure.
To calculate the rectangle value with our corners, we would do the following calculation: $$a \times 8 + b \times 4 + c \times 2 + d \times 1$$
This determines the value, or _isovalue_ as it is commonly referred to as, for a rectangle in this algorithm. 

In this specific image, we have `a = 0`, `b = 1`, `c = 1`, and `d = 1`.
Using our previous formulation, we calculate the value as such: $$0 \times 8 + 1 \times 4 + 1 \times 2 + 1 \times 2 = 7$$.
Now that we have our value, we can then determine how a line inside of the rectangle.
As part of the Marching Squares algorithm, there is a lookup table that defines 16 different cases based on the values calculated.
Here are the various cases:

![](/assets/square_cases.png)
{: style="text-align: center;"}

In our example above, we would use Case 7.
We then draw a line from the center of the left edge to the middle of top edge of the rectangle like this:

![](/assets/square_edge_example.png)
{: style="text-align: center;"}

Let's go ahead and calculate each rectangle's isovalue in the grid!
For convenience, lets define a small function that calculates the isovalue for each rectangle.

```julia
iso_value(a, b, c, d) = a * 8 + b * 4 + c * 2 + d * 1
```

Moving on from there, we can then use the following code snippet to index each value in our `points` array to determine the values for `a`, `b`, `c`, and `d` and calculate each rectangles' isovalue:

```julia
nrows, ncols = size(points)
sethue("black")
for j = 1:(nrows - 1)
    for i = 1:(ncols - 1)
       a = points[j, i]
       b = points[j, i + 1]
       c = points[j + 1, i + 1]
       d = points[j + 1, i]

       case = iso_value(a.val, b.val, c.val, d.val)
       fontsize(14)
       textcentered(string(case), Point((a.x + c.x) / 2, (a.y + c.y) / 2))
    end
end
finish()
```

This snippet produces the following image:

![](/assets/numbering_squares.png)
{: style="text-align: center;"}

Hooray!
We now know the case for each rectangle.
But... How do we actually draw the lines inside of our grid? 
Thankfully, our `draw_balls` algorithm gives us the ability to do just that!

> **NOTE: What is `finish()`?**
>
> `finish()` is a `Luxor` function which tells `Luxor` that we are done drawing on the `Drawing` object and to save the `Drawing` as a file.

## Using Cardinal Directions :bird:

Using our `points` array, we can calculate the center point of each edge on a rectangle.
Taking our previous code snippet, we can modify it slightly to calculate the center of each rectangular edge:

```julia
nrows, ncols = size(points)
sethue("black")
for j = 1:(nrows - 1)
    for i = 1:(ncols - 1)
       a = points[j, i]
       b = points[j, i + 1]
       c = points[j + 1, i + 1]
       d = points[j + 1, i]

       north = Point((b.x + a.x) / 2, a.y)
       east = Point(b.x, (b.y + c.y) / 2)
       south = Point((b.x + a.x) / 2, c.y)
       west = Point(a.x, (a.y + d.y) / 2)
            
       circle(north, 2, :fill)
       circle(east, 2, :fill)
       circle(south, 2, :fill)
       circle(west, 2, :fill)

       case = iso_value(a.val, b.val, c.val, d.val)
       fontsize(14)
       textcentered(string(case), Point((a.x + c.x) / 2, (a.y + c.y) / 2))
    end
end
finish()
```


In this situation, I call the top edge of the rectangle `north`, the right edge, `east`, the bottom edge, `south`, and the left edge, `west`.
The center of each of these edges are represented as a small circle shown in the following diagram:

![](/assets/cardinal_squares.png)
{: style="text-align: center;"}

Now that we have calculated each of the isovalues, let's draw the lines in each of the rectangles to separate the black and white circles!

## Creating Outlines :pencil:

Finally, we can draw the lines, technically called isolines, in each rectangle.
Based on the marching squares cases, let's create a function that defines these cases for us and draws these lines:

```julia
function iso_line(case_value, north, east, south, west)
    if case_value == 0 || case_value == 15
    elseif case_value == 1
        line(west, south, :stroke)
    elseif case_value == 2
        line(south, east, :stroke)
    elseif case_value == 3 || case_value == 12
        line(east, west, :stroke)
    elseif case_value == 4 || case_value == 11
        line(north, east, :stroke)
    elseif case_value == 5
        line(north, west, :stroke)
        line(south, east, :stroke)
    elseif case_value == 6 || case_value == 9
        line(north, south, :stroke)
    elseif case_value == 7 || case_value == 8
        line(north, west, :stroke)
    elseif case_value == 10
        line(north, east, :stroke)
        line(south, west, :stroke)
    elseif case_value == 13
        line(east, south, :stroke)
    elseif case_value == 14
        line(west, south, :stroke)
    end
end
```

This takes in an isovalue and the points we want to draw lines between on each rectangle.
Furthermore, let's finally turn our snippet that we have been building into a function as well to do this all for us:

```julia
function marching_squares(points)
    nrows, ncols = size(points)
    sethue("black")
    for j = 1:(nrows - 1)
        for i = 1:(ncols - 1)
            a = points[j, i]
            b = points[j, i + 1]
            c = points[j + 1, i + 1]
            d = points[j + 1, i]

            north = Point((b.x + a.x) / 2, a.y)
            east = Point(b.x, (b.y + c.y) / 2)
            south = Point((b.x + a.x) / 2, c.y)
            west = Point(a.x, (a.y + d.y) / 2)

            circle(north, 2, :fill)
            circle(east, 2, :fill)
            circle(south, 2, :fill)
            circle(west, 2, :fill)

            case = iso_value(a.val, b.val, c.val, d.val)

            fontsize(14)
            textcentered(string(case), Point((a.x + c.x) / 2, (a.y + c.y) / 2))

            iso_line(case, north, east, south, west)
        end
    end
end
```

The `marching_squares` function takes in the points we calculated from `draw_balls` and creates the boundaries between each white and black ball.
Let's see the final product shall we?

![](/assets/iso_lines_squares.png)
{: style="text-align: center;"}

## The Finished Marching Squares Algorithm :tada:

The previous image was a little cluttered with all the text and additional circles.
I cleaned it up a bit and removed the text from the final image to give this final image:

![](/assets/squares.png)
{: style="text-align: center;"}

Great work! 
You have successfully implemented the marching squares algorithm! :tada: :tada: :tada:

# Concluding Remarks

This algorithm has utility in multiple different places.
Originally, one of the primary usages of the algorithm was for land topography:

![](/assets/topoplot_osm.png)
{: style="text-align: center;"}

If you can see the faint contours in this image provided by [OpenStreetMap](https://www.openstreetmap.org/), these represent different heights of mountain ranges in the Swiss Alps!

Furthermore, people now also use this algorithm for things like video game design as well.
In a post called ["Squares Made for Marching"](https://www.omiod.com/docs/pdf/Squares-Made-for-Marching.pdf) by Andrea Doimo, it is shown how a game map can be automated via this algorithm:

![](/assets/doimo_squares.png)
{: style="text-align: center;"}

Finally, one can also use interpolation to make the edges of the boundaries better fit to the data you are processing.
Check out ["Metaballs and Marching Squares"](http://jamie-wong.com/2014/08/19/metaballs-and-marching-squares/#liinear-interpolation) by Jamie Wong for more examples; here is what he made with his marching squares implementation:

![](/assets/metaballs.png)

I hope this tutorial was a fun introduction to marching squares and that you learned more about this algorithm and how to implement it in Julia!
Now, onto me trying to apply this algorithm to brain data!
Here we go!

Take care and all the best! ~ jz

_If you spot any errors or have any questions, feel free to [contact me](/contact/) about them!_

# Full Code

If at any point in this tutorial you got stuck, here is a copy of the fully operational code.
This code, however, creates a grid for you so you don't have to give it a grid yourself.
If you want to provide your own grid, you just need to replace the `create_grid` with the `draw_balls` function from the tutorial.
Have fun and feel free to tweak this code however you want! 

```julia
#=

Copyright 2020 Jacob Zelko (aka TheCedarPrince)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

=#

using Luxor

function make_drawing(width, height, img_path, bkg_color, origin_p)
    d = Drawing(width, height, img_path)
    background(bkg_color)
    origin(Point(0, 0))
    return d
end

function iso_line(case_value, north, east, south, west)
    if case_value == 0 || case_value == 15
    elseif case_value == 1
        line(west, south, :stroke)
    elseif case_value == 2
        line(south, east, :stroke)
    elseif case_value == 3 || case_value == 12
        line(east, west, :stroke)
    elseif case_value == 4 || case_value == 11
        line(north, east, :stroke)
    elseif case_value == 5
        line(north, west, :stroke)
        line(south, east, :stroke)
    elseif case_value == 6 || case_value == 9
        line(north, south, :stroke)
    elseif case_value == 7 || case_value == 8
        line(north, west, :stroke)
    elseif case_value == 10
        line(north, east, :stroke)
        line(south, west, :stroke)
    elseif case_value == 13
        line(east, south, :stroke)
    elseif case_value == 14
        line(west, south, :stroke)
    end
end

iso_value(a, b, c, d) = a * 8 + b * 4 + c * 2 + d * 1

function create_grid(drawing, nrows, ncols)
    step_x = drawing.width / (ncols - 1)
    step_y = drawing.height / (nrows - 1)
    circ_scale = min(nrows, ncols) / max(nrows, ncols)
    points = Array{NamedTuple}(undef, nrows, ncols)
    for j = 1:nrows
        for i = 1:ncols
            cvalue = rand([0, 1])
            cvalue == 0 ? sethue("white") : sethue("black")
            pos = Point(step_x * (i - 1), step_y * (j - 1))
            circle(pos, 6 * circ_scale, :fill)
            points[j, i] = (x = pos.x, y = pos.y, val = cvalue)
        end
    end
    return points
end

function marching_squares(points)
    nrows, ncols = size(points)
    sethue("black")
    for j = 1:(nrows - 1)
        for i = 1:(ncols - 1)
            a = points[j, i]
            b = points[j, i + 1]
            c = points[j + 1, i + 1]
            d = points[j + 1, i]

            north = Point((b.x + a.x) / 2, a.y)
            east = Point(b.x, (b.y + c.y) / 2)
            south = Point((b.x + a.x) / 2, c.y)
            west = Point(a.x, (a.y + d.y) / 2)

            # circle(north, 2, :fill)
            # circle(east, 2, :fill)
            # circle(south, 2, :fill)
            # circle(west, 2, :fill)

            case = iso_value(a.val, b.val, c.val, d.val)

            # fontsize(14)
            # textcentered(string(case), Point((a.x + c.x) / 2, (a.y + c.y) / 2))

            iso_line(case, north, east, south, west)
        end
    end
end

width = 500
height = 500

nrows = 25
ncols = 25

my_draw = make_drawing(
    width,
    height,
    "squares.png"
    "gray",
    Point(0, 0),
)
grid = create_grid(my_draw, nrows, ncols)

marching_squares(grid)
finish();
```
