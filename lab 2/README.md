### My strategy
This method is divided in two steps: searching best move and making the last move to win:
- in the first one initially i search the move with a nim_sum = 1, if it doesn't find it, it takes the move nearest to nim_sum from one, except the 0, and then do a normal randomization of this move, for example if it takes the move row=2 objs=1 and nim_sum=3, we assume that it knows the number of total object in that moment, it will find a move near to objs 1 in row 2 (it's more probable objs 2 row 2 then objs 3 row 2, because the first is nearest)
- the function move to win is a simply function that makes a check if the rows with objects are 2 or 1. If there are only 2 rows and in one of 2 row there is only an object it will remove all objects in the other row. If there is only one row, if it is possible it will make the move that leaves only one object, instead if it is only one object it will remove it knowing that it has lost:(

It has a very good performance and a little part of this good performance is given by the move_to_win function, indeed this has increased the percentage of winning vs the optimal method. From about 63% to about 78%

percentage of win rate:
- my_strategy vs optimal: 78% vs 22%
- my_strategy vs pure_random: 89% vs 11%
- my_strategy vs gabriele: 99% vs 1%