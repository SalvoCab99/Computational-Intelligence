# Q-learning algorithm
In this lab I used a reinforcement learning(RL) approach.
I created a dictionary that has the current situation (state) as index and best action and its feedback as values.
In the training section this dictionary will be filled and it will be used when it plays.
The feedback value is given by the formula (1 - alpha)* value_dictionary[(state_key, action)] + alpha * (reward+ discount_factor*max_next_value).
when we train the player as "X" it is able only for playing with that. Same thing when we train it as "O", it can only play with "O"


The results that I show are given by 10_000 games:

- my player = "X":
- Results for 10_000 games:
    - Win rate of our player(9149): 91.49%
    - Win rate of random player(618): 6.18%
    - Draw rate(233): 2.33%

- my player = "O":
- Results for 10_000 games:
    - Win rate of our player(7807): 78.07%
    - Win rate of random player(1849): 18.49%
    - Draw rate(344): 3.44%

Reviewed: [Luca Pastore](https://github.com/s288976/computational_intelligence_23_24/issues/2#issue-2067837272) and [Marcello Vitaggio](https://github.com/Kalller/computational-intelligence/issues/6#issue-2067758806)