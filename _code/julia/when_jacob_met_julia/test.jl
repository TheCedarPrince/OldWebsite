# Directly loads in the Plots.jl module for plotting 
using Plots

# Selecting GR as the backend for Plots 
gr()

# Generating 20 random data 
x = 1:20
y = rand(20)

# Plots random data to line plot
plot(x, y)