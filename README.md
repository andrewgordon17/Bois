# Bois
Bois is an awful backronym for Basic Orienting Individuals. The goal of this project is to translate local data into global geometric structures.

The general problem is to imagine robots on a coordinate plane. Each robot can see its immediate neighbors, but nothing beyond. Each robot should be identical in terms of description and the code it executes. Given this, can a group of such robots execute complex behaviors?

There are many questions you could pose here: Could the robots form larger shapes, or single out one robot (the northmost, the most central, etc) I have implementeed most of a solution to the problem of lining up. When bois_plot is run, it creates a swarm that, despite each boi seeing only a small radius, coalesces into a straight line. The different files are organized as follows

bois_plot: the visual. This calls the other files and creates a visual of the bois moving around.

bois_classes: This contains the definitions for the various objects used. There is very little that is algorithmically interesting here

movement functions: A list of possible functions to be used to initialize boi objects. the most noteworthy at the moment is line_find_best_fit
