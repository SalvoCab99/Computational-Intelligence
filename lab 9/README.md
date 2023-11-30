### Evolutionary algorithm
I made a solution with a standard evolutionary algorithm approach.
The population size is 100, so it will be created 100 individuals and their fitness will be calculated, then it will be popolated thanks to the mutation and crossover functions.
There is a counter used to count the numer of times that the best fitness function is the same; this provides to stop populating when we suppose to have reached the best fitness of that problem. The number is not randomly selected, because I tested different value and 150 for a NUM_SETS = 1000 is a good compromise

## Mutation
There are 3 mutation functions:
- `mutate`: it's a standard mutation, one element is randomly selected and its value will change (0->1 or 1->0).
- `n_mutate`: it's similar to the previous one, but it takes in input an `n` that will be the number of elements will be selected for the changing. `n` is a number given by a random function in a range of 2 and `NUM_SETS`/10. `NUM_SETS` is the numbers of elements in the individual genotype.
- `little_reverse`: this function reverse a slice of the elements, this slice is randomly selected and the lenght is also randomly selected in a range of 2 and `NUM_SETS`/10

## Crossover
There are 3 crossover functions:
- `one_cut_xover`: it's a very standard crossover, one point is randomly selected and the part between 0 and the point is given by the first parent and the part between the point and the end is given by the second parent
- `n_cut_xover`: it's similar to the previous one, but it takes in input an `n` that will be the number of point that will be cut the individual genotype. When all point will be radomly selected the new individual will be alternately the first parent and the second one. `n` is a number given by a random function in a range of 2 and `NUM_SETS`/10. `NUM_SETS` is the numbers of elements in the individual genotype.
- `uniform_xover`: it's a standard crossove, each element of the new individual is randomly given by the first parent or the second parent

### RESULTS
dire che con solo mutate è migliore quando il problem size è piccolo e aggiungere risultati