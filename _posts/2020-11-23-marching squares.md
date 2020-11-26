---
title: "Naive Implementation of Marching Squares"
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

For reference going forward, we will be using this $$10 \times 10$$ grid where I have already applied a threshold and converted all values to $$0$$'s and $$1$$'s:

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

To process this information and implement the algorithm 



Essentially, how it works is you make a matrix of points. 
I chose to have 10 rows and columns of points. 
I accomplished this with Luxor.jl - a wonderful #Graphics library created by Cormullion (link: https://github.com/JuliaGraphics/Luxor.jl) in Julia that builds on top of Cairo.


asdf


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

