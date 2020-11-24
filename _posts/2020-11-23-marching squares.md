---
title: "Simple Implementation of Marching Squares"
image:
  path: /assets/squares_banner.png
comments: true
share: true
tags:
    - julia
    - algorithms
---

Essentially, how it works is you make a matrix of points. 
I chose to have 10 rows and columns of points. 
I accomplished this with Luxor.jl - a wonderful #Graphics library created by Cormullion (link: https://github.com/JuliaGraphics/Luxor.jl) in Julia that builds on top of Cairo.

!!! SHOW BASIC 10 x 10 GRID !!!

From there, we determine specific cases based on the smaller squares formed inside the previous grid (each of the four points).
More on this here: https://wikiwand.com/en/Marching_squares#/Basic_algorithm

I determine the case and associate each square with the case value.

!!! SHOWING CASE VALUES !!! 

Now, we need to determine how to draw the lines!
We have the case numbers, but how do we actually #plot the lines? 
For this, I calculate the cardinal locations in each square: north, east, south, and west.

These are represented small circles on this plot!

!!! SHOWING CASE VALUES WITH CARDINAL DIRECTIONS !!!

Finally, we can draw the, lines, technically, isolines by connecting each of these cardinal locations based on each squares case!

This yields our boundaries around the white and black balls:

!!! EVERYTHING ALTOGETHER !!!


